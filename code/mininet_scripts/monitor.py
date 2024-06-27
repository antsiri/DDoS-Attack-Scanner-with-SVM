# Il seguente codice permette di aggiungere al Simple_Switch_13 (aka Controller) 
# di aggiungere le funzioni di monitoraggio della rete

from operator import attrgetter

from ryu.app import simple_monitor_13
from ryu.controller import ofp_event
from ryu.controller.handler import MAIN_DISPATCHER, DEAD_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.lib import hub

class SimleMonitor13(simple_monitor_13.SimpleMonitor13):
    # Parallelamente all'hub switchiung, si crea un thread per emettere perodicamente
    #  allo switch OperFlow di acquisire informazioni statistiche.

    def __init__(self, *args, **kwargs):
        super(SimleMonitor13, self).__init__(*args, **kwargs)
        self.datapaths = {}
        self.monitor_thread = hub.spawn(self._monitor)          #creazione threads

    #----------------------------------------------------------------------------------------------------- 
    # Nella funzione _monitor, viene effettuata una richesta di acquisizione delle informazioni 
    # per lo switch registrato ogni 10 secondi. 
    # 
    # Per assicurarsi che lo switch sia monitorato, l'evento EventoOFPStateChange viene utilizzato per
    # rilevare la connessione e la disconnessione: viene emesso da Ryu quando viene modicato lo stato del
    # datapath.
    # 
    # Quando lo stato del datapath è MAIN_DISPATCHER, quello switch è registrato come target del monitor
    # mentre quando è DEAD_DISPATCHER la registrazione viene cancellata.
    #
    # Con la chaimata periodica di _request_stats, OFPFlowStatsRequest e OFPPortStatsRequest vengono 
    # emessi allo switch.

    @set_ev_cls(ofp_event.EventOFPStateChange, [MAIN_DISPATCHER, DEAD_DISPATCHER])
    def _state_change_handler(self, ev):
        datapath = ev.datapath
        if ev.state == MAIN_DISPATCHER:
            if datapath.id not in self.datapaths:
                self.logger.debug('register datapath: %016x', datapath.id)
                self.datapaths[datapath.id] = datapath
        elif ev.state == DEAD_DISPATCHER:
            if datapath.id in self.datapaths:
                self.logger.debug('unregister datapath: %016x', datapath.id)
                del self.datapaths[datapath.id]

    def _monitor(self):
        while True:
            for dp in self.datapaths.values():
                self._request_stats(dp)
            hub.sleep(10)

    def _request_stats(self, datapath):
        self.logger.debug('send stats request: %016x', datapath.id)
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        # richiesta allo switch di fornire le informazioni statistiche relative al flusso
        req = parser.OFPFlowStatsRequest(datapath)
        datapath.send_msg(req)

        # richiesta allo switch sulle inforamazioni statistiche relative ad ogni porto
        req = parser.OFPPortStatsRequest(datapath, 0, ofproto.OFPP_ANY)
        datapath.send_msg(req)
    
    #----------------------------------------------------------------------------------------------------- 
    # Per ricevere una risposta dallo switch, va creato un gestore di aventi che riceve 
    # il messaggio FlowStatsReply.

    @set_ev_cls(ofp_event.EventOFPFlowStatsReply, MAIN_DISPATCHER)  #Memorizzazione delle informazioni del flusso
    def _flow_stats_reply_handler(self, ev):
        body = ev.msg.body

        self.logger.info('datapath          '
                         'in-port   eth-dst             '
                         'out-port  packets     bytes')
        self.logger.info('----------------- '
                         '----------------------------- '
                         '--------  -------     -------')
        for stat in sorted([flow for flow in body if flow.priority == 1],   #Vengono selezionate tutte le voci di flusso eccetto quelle del Table-miss (0)
                           key=lambda flow: (flow.match['in_port'],         #Ordinamento in base al porto e all'indirizzo MAC di destinazione 
                                             flow.match['eth_dst'])):
            self.logger.info('%016x %8x %17s %8x %8d %8d',
                             ev.msg.datapath.id,
                             stat.match['in_port'], stat.match['eth_dst'],
                             stat.instructions[0].actions[0].port,
                             stat.packet_count, stat.byte_count)

    #----------------------------------------------------------------------------------------------------- 
    # Si ripete lo stesso procedimnento ma per ogni singolo porto

    @set_ev_cls(ofp_event.EventOFPPortStatsReply, MAIN_DISPATCHER)
    def _port_stats_reply_handler(self, ev):
        body = ev.msg.body
        
        self.logger.info('datapath          port        '
                         'rx-pkts   rx-bytes    rx-error'
                         'tx-pkts   tx-bytes    tx-error')
        self.logger.info('----------------- ----------- '
                         '-------   --------    --------'
                         '-------   --------    --------')
        for stat in sorted(body, key=attrgetter('port_no')):
            self.logger.info('%016x %8x %8d %8d %8d %8d %8d %8d', 
                             ev.msg.datapath.id, stat.port_no, 
                             stat.rx_packets, stat.rx_bytes, stat.rx_errors,
                             stat.tx_packets, stat.tx_bytes, stat.tx_errors)
