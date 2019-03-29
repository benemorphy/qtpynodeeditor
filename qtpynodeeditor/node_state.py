from collections import OrderedDict

from .enums import ReactToConnectionState
from .base import ConnectionBase
from .node_data import NodeDataType
from .port import PortType, Port


class NodeState:
    def __init__(self, node):
        '''
        node_state

        Parameters
        ----------
        model : NodeDataModel
        '''
        self._ports = {PortType.input: OrderedDict(),
                       PortType.output: OrderedDict()
                       }

        model = node.model
        for port_type in self._ports:
            num_ports = model.num_ports[port_type]
            self._ports[port_type] = OrderedDict(
                (i, Port(node, port_type=port_type, index=i))
                for i in range(num_ports)
            )

        self._reaction = ReactToConnectionState.not_reacting
        self._reacting_port_type = PortType.none
        self._reacting_data_type = None
        self._resizing = False

    def __getitem__(self, key):
        return self._ports[key]

    @property
    def ports(self):
        yield from self.input_ports
        yield from self.output_ports

    @property
    def input_ports(self):
        yield from self[PortType.input].values()

    @property
    def output_ports(self):
        yield from self[PortType.output].values()

    @property
    def all_connections(self):
        return [connection
                for port_type, ports in self._ports.items()
                for idx, port in ports.items()
                for connection in port.connections
                ]

    def connections(self, port_type: PortType, port_index: int) -> list:
        """
        Connections

        Parameters
        ----------
        port_type : PortType
        port_index : int

        Returns
        -------
        value : list
        """
        return list(self._ports[port_type][port_index].connections)

    def erase_connection(self, port_type: PortType, port_index: int, connection: ConnectionBase):
        """
        Erase connection

        Parameters
        ----------
        port_type : PortType
        port_index : int
        connection : Connection
        """
        self._ports[port_type][port_index].remove_connection(connection)

    @property
    def reaction(self) -> ReactToConnectionState:
        """
        Reaction

        Returns
        -------
        value : NodeState.ReactToConnectionState
        """
        return self._reaction

    @property
    def reacting_port_type(self) -> PortType:
        """
        Reacting port type

        Returns
        -------
        value : PortType
        """
        return self._reacting_port_type

    @property
    def reacting_data_type(self) -> NodeDataType:
        """
        Reacting data type

        Returns
        -------
        value : NodeDataType
        """
        return self._reacting_data_type

    def set_reaction(self, reaction: ReactToConnectionState,
                     reacting_port_type: PortType = PortType.none,
                     reacting_data_type: NodeDataType = None):
        """
        Set reaction

        Parameters
        ----------
        reaction : NodeState.ReactToConnectionState
        reacting_port_type : PortType, optional
        reacting_data_type : NodeDataType
        """
        self._reaction = ReactToConnectionState(reaction)
        self._reacting_port_type = reacting_port_type
        self._reacting_data_type = reacting_data_type

    @property
    def is_reacting(self) -> bool:
        """
        Is the node reacting to a mouse event?

        Returns
        -------
        value : bool
        """
        return self._reaction == ReactToConnectionState.reacting

    @property
    def resizing(self) -> bool:
        """
        Resizing

        Returns
        -------
        value : bool
        """
        return self._resizing

    @resizing.setter
    def resizing(self, resizing: bool):
        self._resizing = resizing
