import React, { useState, useEffect, useRef } from 'react';
import { 
  Activity, 
  Shield, 
  AlertTriangle, 
  Zap, 
  Share2, 
  Send, 
  Cpu, 
  Lock, 
  FileText, 
  Database,
  RefreshCw
} from 'lucide-react';

interface Transaction {
  transaction_id: string;
  source_account: string;
  target_account: string;
  amount: number;
  currency: string;
  mode: string;
  timestamp: string;
  device_id?: string;
  ip_address?: string;
}

interface ScoreResult {
  risk_score: number;
  is_fraud: boolean;
}

interface EventData {
  event_type: string;
  transaction: Transaction;
  result: ScoreResult;
}

interface BlockchainSeal {
  transaction_id: string;
  seal_id: string;
  status: string;
  timestamp: string;
}

export default function App() {
  const [wsConnected, setWsConnected] = useState<boolean>(false);
  const [transactions, setTransactions] = useState<EventData[]>([]);
  const [selectedTxn, setSelectedTxn] = useState<EventData | null>(null);
  
  // Quick-inject transaction form state
  const [sourceAccount, setSourceAccount] = useState<string>('ACC987654321');
  const [targetAccount, setTargetAccount] = useState<string>('ACC123456789');
  const [amount, setAmount] = useState<string>('250.00');
  const [mode, setMode] = useState<string>('UPI');
  const [loadingInject, setLoadingInject] = useState<boolean>(false);
  const [injectStatus, setInjectStatus] = useState<string | null>(null);
  
  // Operations state
  const [blockchainSeals, setBlockchainSeals] = useState<BlockchainSeal[]>([]);
  const [sealingId, setSealingId] = useState<string | null>(null);
  const [honeypots, setHoneypots] = useState<string[]>([]);
  const [tps, setTps] = useState<number>(0);

  const socketRef = useRef<WebSocket | null>(null);
  const reconnectTimeoutRef = useRef<number | null>(null);

  // WebSocket lifecycle management
  useEffect(() => {
    const connectWs = () => {
      const clientId = `client_${Math.random().toString(36).substring(7)}`;
      // Connect to modular WebSocket route
      const wsUrl = `ws://localhost:8000/api/v1/fraud/stream/${clientId}`;
      console.log(`Connecting to WebSocket: ${wsUrl}`);
      const socket = new WebSocket(wsUrl);
      socketRef.current = socket;

      socket.onopen = () => {
        console.log('WebSocket connection established');
        setWsConnected(true);
        setInjectStatus('Stream connected');
        
        // Start ping loop
        const pingInterval = setInterval(() => {
          if (socket.readyState === WebSocket.OPEN) {
            socket.send('ping');
          }
        }, 15000);
        
        return () => clearInterval(pingInterval);
      };

      socket.onmessage = (event) => {
        if (event.data === 'pong') return;
        
        try {
          const data: EventData = JSON.parse(event.data);
          if (data.event_type === 'transaction_scored') {
            setTransactions(prev => {
              const updated = [data, ...prev].slice(0, 15);
              return updated;
            });
            // Automatically select the first/newest transaction if none is selected
            setSelectedTxn(prev => prev || data);
          }
        } catch (err) {
          console.error('Error parsing WebSocket message:', err);
        }
      };

      socket.onclose = () => {
        console.log('WebSocket connection closed. Attempting reconnect...');
        setWsConnected(false);
        reconnectTimeoutRef.current = window.setTimeout(connectWs, 3000);
      };

      socket.onerror = (err) => {
        console.error('WebSocket error:', err);
        socket.close();
      };
    };

    connectWs();

    return () => {
      if (socketRef.current) socketRef.current.close();
      if (reconnectTimeoutRef.current) clearTimeout(reconnectTimeoutRef.current);
    };
  }, []);

  // Compute live statistics and TPS
  useEffect(() => {
    // Basic moving TPS indicator
    const interval = setInterval(() => {
      setTps(() => {
        const count = transactions.filter(t => {
          const tTime = new Date(t.transaction.timestamp).getTime();
          return Date.now() - tTime < 10000;
        }).length;
        return parseFloat((count / 10).toFixed(2));
      });
    }, 2000);

    return () => clearInterval(interval);
  }, [transactions]);

  const totalProcessed = transactions.length;
  const totalBlocked = transactions.filter(t => t.result.is_fraud).length;
  const totalReview = transactions.filter(t => !t.result.is_fraud && t.result.risk_score >= 50.0).length;
  const avgRisk = totalProcessed > 0 
    ? Math.round(transactions.reduce((sum, t) => sum + t.result.risk_score, 0) / totalProcessed) 
    : 0;

  // Manual transaction injection handler
  const handleInject = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoadingInject(true);
    setInjectStatus('Submitting payload...');

    const transaction_id = `TXN_DEV_${Math.floor(Math.random() * 900000 + 100000)}`;
    const payload = {
      transaction_id,
      source_account: sourceAccount,
      target_account: targetAccount,
      amount: parseFloat(amount),
      currency: 'INR',
      mode,
      timestamp: new Date().toISOString(),
      device_id: `DEV_${Math.floor(Math.random() * 900 + 100)}`,
      ip_address: `192.168.1.${Math.floor(Math.random() * 254 + 1)}`
    };

    try {
      const response = await fetch('http://localhost:8000/api/v1/stream/ingest', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
      });

      if (response.ok) {
        await response.json();
        setInjectStatus(`Ingested: ${transaction_id}`);
      } else {
        const errData = await response.json();
        setInjectStatus(`Failed: ${errData.detail || response.statusText}`);
      }
    } catch (err: any) {
      setInjectStatus(`Error: ${err.message}`);
    } finally {
      setLoadingInject(false);
    }
  };

  // Quick helper to fill dummy transaction structures
  const loadRandomTransaction = () => {
    const src = `ACC${Math.floor(Math.random() * 900000 + 100000)}`;
    const tgt = `ACC${Math.floor(Math.random() * 900000 + 100000)}`;
    // 15% probability of huge anomalous amounts
    const val = Math.random() < 0.15 
      ? (Math.random() * 85000 + 15000).toFixed(2) 
      : (Math.random() * 1200 + 50).toFixed(2);
    const modes = ['UPI', 'IMPS', 'NEFT', 'RTGS', 'CARD'];

    setSourceAccount(src);
    setTargetAccount(tgt);
    setAmount(val);
    setMode(modes[Math.floor(Math.random() * modes.length)]);
  };

  // Seal blockchain evidence handler
  const handleBlockchainSeal = async (txnId: string) => {
    setSealingId(txnId);
    try {
      const response = await fetch('http://localhost:8000/api/v1/blockchain/seal', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ data: `AEGIS-EVIDENCE-TXN-${txnId}-CONFIRM` })
      });

      if (response.ok) {
        const res = await response.json();
        setBlockchainSeals(prev => [
          {
            transaction_id: txnId,
            seal_id: res.seal_id,
            status: 'sealed',
            timestamp: new Date().toLocaleTimeString()
          },
          ...prev
        ]);
      }
    } catch (err) {
      console.error('Blockchain sealing failed:', err);
    } finally {
      setSealingId(null);
    }
  };

  // Trigger honeypot trap handler
  const handleHoneypotTrigger = (txnId: string) => {
    if (honeypots.includes(txnId)) {
      setHoneypots(prev => prev.filter(id => id !== txnId));
    } else {
      setHoneypots(prev => [...prev, txnId]);
    }
  };

  // SVG Graph Coordinate Calculators
  const nodesMap = new Map<string, { x: number; y: number; isHighRisk: boolean }>();
  const edges: { source: string; target: string; isHighRisk: boolean; score: number }[] = [];

  transactions.forEach((t, i) => {
    const src = t.transaction.source_account;
    const tgt = t.transaction.target_account;
    const isHighRisk = t.result.risk_score >= 50.0;

    if (!nodesMap.has(src)) {
      // Deterministic layout based on hashing string to index around the canvas
      const angle = (i * 2.4) + 0.5;
      const radius = 100 + (i * 4) % 60;
      nodesMap.set(src, {
        x: 250 + Math.cos(angle) * radius,
        y: 180 + Math.sin(angle) * radius,
        isHighRisk
      });
    } else if (isHighRisk) {
      nodesMap.get(src)!.isHighRisk = true;
    }

    if (!nodesMap.has(tgt)) {
      const angle = (i * 2.4) + 1.7;
      const radius = 120 + (i * 3) % 40;
      nodesMap.set(tgt, {
        x: 250 + Math.cos(angle) * radius,
        y: 180 + Math.sin(angle) * radius,
        isHighRisk
      });
    } else if (isHighRisk) {
      nodesMap.get(tgt)!.isHighRisk = true;
    }

    edges.push({
      source: src,
      target: tgt,
      isHighRisk,
      score: t.result.risk_score
    });
  });

  return (
    <div className="min-h-screen bg-[#09090b] flex flex-col">
      {/* Top Banner Navigation */}
      <header className="border-b border-[#27272a] bg-[#18181b]/60 backdrop-blur-md sticky top-0 z-30 px-6 py-4 flex items-center justify-between">
        <div className="flex items-center space-x-3">
          <div className="p-2 bg-blue-500/10 border border-blue-500/20 rounded-lg text-blue-500">
            <Shield className="w-6 h-6 animate-pulse" />
          </div>
          <div>
            <h1 className="font-bold text-lg tracking-wider text-white">AEGIS SENTINEL 2.0</h1>
            <p className="text-xs text-zinc-500">Enterprise AI Fraud Intelligence Ecosystem</p>
          </div>
        </div>

        {/* Real-time Status Connection Bar */}
        <div className="flex items-center space-x-6">
          <div className="flex items-center space-x-2 bg-zinc-900 border border-zinc-800 rounded-full px-4 py-1.5 text-xs text-zinc-300">
            <span className={`w-2.5 h-2.5 rounded-full ${wsConnected ? 'bg-green-500 animate-ping' : 'bg-red-500'}`} />
            <span>{wsConnected ? 'API WebSocket Stream Active' : 'API Connecting...'}</span>
          </div>

          <div className="text-right">
            <span className="text-xs text-zinc-500 block">Ingestion Rate</span>
            <span className="text-sm font-semibold text-white flex items-center justify-end gap-1">
              <Zap className="w-3.5 h-3.5 text-yellow-500 fill-yellow-500" />
              {tps} TPS
            </span>
          </div>
        </div>
      </header>

      {/* Main Operations Matrix Layout */}
      <main className="flex-1 p-6 grid grid-cols-12 gap-6 max-w-7xl mx-auto w-full">
        {/* Realtime Metrics Summary Grid */}
        <section className="col-span-12 grid grid-cols-4 gap-4">
          <div className="bg-[#18181b] border border-[#27272a] rounded-xl p-4 flex items-center justify-between shadow-lg">
            <div>
              <span className="text-xs text-zinc-500 font-medium">TOTAL PROCESSED</span>
              <p className="text-2xl font-bold text-zinc-100 mt-1">{totalProcessed}</p>
            </div>
            <Activity className="w-8 h-8 text-zinc-600" />
          </div>

          <div className="bg-[#18181b] border border-[#27272a] rounded-xl p-4 flex items-center justify-between shadow-lg">
            <div>
              <span className="text-xs text-red-500 font-medium">FRAUD BLOCKED</span>
              <p className="text-2xl font-bold text-red-500 mt-1">{totalBlocked}</p>
            </div>
            <AlertTriangle className="w-8 h-8 text-red-500/20" />
          </div>

          <div className="bg-[#18181b] border border-[#27272a] rounded-xl p-4 flex items-center justify-between shadow-lg">
            <div>
              <span className="text-xs text-yellow-500 font-medium">MANUAL REVIEWS</span>
              <p className="text-2xl font-bold text-yellow-500 mt-1">{totalReview}</p>
            </div>
            <AlertTriangle className="w-8 h-8 text-yellow-500/20" />
          </div>

          <div className="bg-[#18181b] border border-[#27272a] rounded-xl p-4 flex items-center justify-between shadow-lg">
            <div>
              <span className="text-xs text-blue-500 font-medium">AVG RISK SCORE</span>
              <p className="text-2xl font-bold text-blue-400 mt-1">{avgRisk}%</p>
            </div>
            <Shield className="w-8 h-8 text-blue-500/20" />
          </div>
        </section>

        {/* Panel 1: Live Transactions Feed */}
        <section className="col-span-4 bg-[#18181b] border border-[#27272a] rounded-xl p-4 flex flex-col shadow-xl h-[620px]">
          <h2 className="text-sm font-bold text-zinc-300 tracking-wider mb-3 flex items-center gap-2">
            <RefreshCw className="w-4 h-4 text-blue-500 animate-spin" />
            LIVE SECURITY STREAM
          </h2>

          <div className="flex-1 overflow-y-auto pr-2 space-y-3">
            {transactions.length === 0 ? (
              <div className="h-full flex flex-col items-center justify-center text-center text-zinc-600">
                <Database className="w-12 h-12 mb-2 animate-bounce" />
                <p className="text-xs">Waiting for stream transaction inputs...</p>
                <button 
                  onClick={loadRandomTransaction}
                  className="mt-4 px-3 py-1.5 text-xs text-blue-500 hover:text-blue-400 font-semibold border border-blue-500/20 hover:border-blue-500/40 rounded-lg transition"
                >
                  Load Mock Template
                </button>
              </div>
            ) : (
              transactions.map((txn) => {
                const isSelected = selectedTxn?.transaction.transaction_id === txn.transaction.transaction_id;
                const statusColor = txn.result.is_fraud 
                  ? 'border-red-500/40 hover:border-red-500/80 bg-red-500/5' 
                  : txn.result.risk_score >= 50.0 
                    ? 'border-yellow-500/40 hover:border-yellow-500/80 bg-yellow-500/5'
                    : 'border-green-500/35 hover:border-green-500/70 bg-green-500/5';
                
                return (
                  <div
                    key={txn.transaction.transaction_id}
                    onClick={() => setSelectedTxn(txn)}
                    className={`cursor-pointer p-3 border rounded-xl flex items-start justify-between gap-3 transition-all duration-300 ${statusColor} ${isSelected ? 'ring-2 ring-blue-500 border-transparent shadow-xl' : 'shadow-md'}`}
                  >
                    <div className="flex-1 min-w-0">
                      <span className="text-xs text-zinc-500 font-bold block">{txn.transaction.transaction_id}</span>
                      <div className="text-xs text-zinc-300 mt-1 flex items-center gap-1.5">
                        <span className="font-mono truncate max-w-[80px]">{txn.transaction.source_account}</span>
                        <span className="text-zinc-600">→</span>
                        <span className="font-mono truncate max-w-[80px]">{txn.transaction.target_account}</span>
                      </div>
                      <span className="text-xs text-zinc-400 font-medium block mt-1.5">
                        INR {txn.transaction.amount.toLocaleString()}
                      </span>
                    </div>

                    <div className="text-right">
                      <span className={`text-[10px] px-2 py-0.5 font-bold rounded-full block border ${
                        txn.result.is_fraud 
                          ? 'text-red-400 border-red-500/20 bg-red-500/10' 
                          : txn.result.risk_score >= 50.0 
                            ? 'text-yellow-400 border-yellow-500/20 bg-yellow-500/10'
                            : 'text-green-400 border-green-500/20 bg-green-500/10'
                      }`}>
                        {txn.result.is_fraud ? 'BLOCK' : (txn.result.risk_score >= 50.0 ? 'REVIEW' : 'ALLOW')}
                      </span>
                      <span className="text-xs text-zinc-500 font-bold block mt-1">{txn.result.risk_score}% Risk</span>
                    </div>
                  </div>
                );
              })
            )}
          </div>
        </section>

        {/* Panel 2: SVG Graph Explorer & Form */}
        <section className="col-span-5 flex flex-col gap-6 h-[620px]">
          {/* Visual Graph View */}
          <div className="bg-[#18181b] border border-[#27272a] rounded-xl p-4 flex-1 flex flex-col shadow-xl">
            <h2 className="text-sm font-bold text-zinc-300 tracking-wider mb-2 flex items-center gap-2">
              <Share2 className="w-4 h-4 text-blue-500" />
              GRAPH CHAIN EXPLORER
            </h2>

            <div className="flex-1 border border-zinc-800 bg-zinc-950/70 rounded-xl relative overflow-hidden flex items-center justify-center">
              {transactions.length === 0 ? (
                <span className="text-xs text-zinc-600">No active network nodes</span>
              ) : (
                <svg className="w-full h-full" viewBox="0 0 500 360">
                  {/* Draw edges/transaction links */}
                  {edges.map((e, index) => {
                    const fromNode = nodesMap.get(e.source);
                    const toNode = nodesMap.get(e.target);
                    if (!fromNode || !toNode) return null;
                    const strokeColor = e.isHighRisk ? '#ef4444' : '#22c55e';
                    const strokeWidth = e.isHighRisk ? '2.5' : '1.2';
                    const glowClass = e.isHighRisk ? 'drop-shadow-[0_0_4px_rgba(239,68,68,0.8)]' : '';

                    return (
                      <g key={`edge-${index}`}>
                        <line
                          x1={fromNode.x}
                          y1={fromNode.y}
                          x2={toNode.x}
                          y2={toNode.y}
                          stroke={strokeColor}
                          strokeWidth={strokeWidth}
                          strokeDasharray={e.isHighRisk ? "5, 5" : "none"}
                          className={glowClass}
                        />
                      </g>
                    );
                  })}

                  {/* Draw Nodes */}
                  {Array.from(nodesMap.entries()).map(([name, node]) => {
                    return (
                      <g key={`node-${name}`} className="cursor-pointer">
                        <circle
                          cx={node.x}
                          cy={node.y}
                          r={node.isHighRisk ? "9" : "6"}
                          fill={node.isHighRisk ? '#ef4444' : '#3b82f6'}
                          stroke="#18181b"
                          strokeWidth="2"
                          className={node.isHighRisk ? 'drop-shadow-[0_0_6px_rgba(239,68,68,0.8)]' : ''}
                        />
                        <text
                          x={node.x}
                          y={node.y - 12}
                          textAnchor="middle"
                          fill="#a1a1aa"
                          fontSize="8px"
                          fontWeight="bold"
                          className="font-mono bg-zinc-950 px-1 py-0.5 rounded"
                        >
                          {name.substring(0, 7)}...
                        </text>
                      </g>
                    );
                  })}
                </svg>
              )}

              <div className="absolute bottom-3 left-3 text-[10px] text-zinc-500 bg-zinc-950/80 px-2 py-1 rounded border border-zinc-800 flex gap-4">
                <span className="flex items-center gap-1"><span className="w-2.5 h-2.5 rounded-full bg-red-500" /> High-Risk Node</span>
                <span className="flex items-center gap-1"><span className="w-2.5 h-2.5 rounded-full bg-blue-500" /> Normal Node</span>
              </div>
            </div>
          </div>

          {/* Quick Injector Form */}
          <div className="bg-[#18181b] border border-[#27272a] rounded-xl p-4 shadow-xl">
            <div className="flex items-center justify-between mb-3">
              <h2 className="text-sm font-bold text-zinc-300 tracking-wider flex items-center gap-2">
                <Send className="w-4 h-4 text-blue-500" />
                TRANSACTION INJECTOR
              </h2>
              <button
                type="button"
                onClick={loadRandomTransaction}
                className="text-[10px] text-blue-500 font-bold hover:underline"
              >
                Auto Generate
              </button>
            </div>

            <form onSubmit={handleInject} className="grid grid-cols-2 gap-3">
              <div>
                <label className="text-[10px] text-zinc-500 font-bold block mb-1">SOURCE ACCOUNT</label>
                <input 
                  type="text" 
                  value={sourceAccount}
                  onChange={(e) => setSourceAccount(e.target.value)}
                  className="w-full text-xs bg-zinc-950 border border-zinc-800 rounded-lg p-2 text-zinc-200 font-mono focus:outline-none focus:ring-1 focus:ring-blue-500"
                />
              </div>

              <div>
                <label className="text-[10px] text-zinc-500 font-bold block mb-1">TARGET ACCOUNT</label>
                <input 
                  type="text" 
                  value={targetAccount}
                  onChange={(e) => setTargetAccount(e.target.value)}
                  className="w-full text-xs bg-zinc-950 border border-zinc-800 rounded-lg p-2 text-zinc-200 font-mono focus:outline-none focus:ring-1 focus:ring-blue-500"
                />
              </div>

              <div>
                <label className="text-[10px] text-zinc-500 font-bold block mb-1">AMOUNT (INR)</label>
                <input 
                  type="number" 
                  step="0.01"
                  value={amount}
                  onChange={(e) => setAmount(e.target.value)}
                  className="w-full text-xs bg-zinc-950 border border-zinc-800 rounded-lg p-2 text-zinc-200 font-mono focus:outline-none focus:ring-1 focus:ring-blue-500"
                />
              </div>

              <div>
                <label className="text-[10px] text-zinc-500 font-bold block mb-1">MODE</label>
                <select 
                  value={mode}
                  onChange={(e) => setMode(e.target.value)}
                  className="w-full text-xs bg-zinc-950 border border-zinc-800 rounded-lg p-2 text-zinc-200 focus:outline-none focus:ring-1 focus:ring-blue-500"
                >
                  <option value="UPI">UPI</option>
                  <option value="IMPS">IMPS</option>
                  <option value="NEFT">NEFT</option>
                  <option value="RTGS">RTGS</option>
                  <option value="CARD">CARD</option>
                </select>
              </div>

              <div className="col-span-2 flex items-center justify-between mt-1">
                <span className="text-[10px] text-zinc-500 truncate max-w-[200px]">
                  {injectStatus}
                </span>

                <button 
                  type="submit"
                  disabled={loadingInject}
                  className="bg-blue-500 hover:bg-blue-600 disabled:bg-zinc-700 text-white font-bold text-xs px-4 py-2 rounded-lg flex items-center gap-1.5 transition"
                >
                  <Zap className="w-3.5 h-3.5 fill-current" />
                  Push to Kafka
                </button>
              </div>
            </form>
          </div>
        </section>

        {/* Panel 3: Oracle AI explain & Operations */}
        <section className="col-span-3 bg-[#18181b] border border-[#27272a] rounded-xl p-4 flex flex-col shadow-xl h-[620px]">
          <h2 className="text-sm font-bold text-zinc-300 tracking-wider mb-3 flex items-center gap-2">
            <Cpu className="w-4 h-4 text-blue-500" />
            AEGIS-ORACLE AI LOGS
          </h2>

          {!selectedTxn ? (
            <div className="flex-1 flex items-center justify-center text-center text-zinc-600 text-xs">
              Select a transaction in the live feed to analyze risk factors.
            </div>
          ) : (
            <div className="flex-1 flex flex-col space-y-4 text-xs">
              {/* Score Indicator */}
              <div className="border border-zinc-800 rounded-xl p-3 bg-zinc-950/70">
                <span className="text-[10px] text-zinc-500 font-bold block uppercase">Risk Evaluation Score</span>
                <div className="flex items-baseline gap-2 mt-1">
                  <span className="text-3xl font-black text-white">{selectedTxn.result.risk_score}%</span>
                  <span className={`text-[10px] font-bold ${selectedTxn.result.is_fraud ? 'text-red-500' : 'text-green-500'}`}>
                    {selectedTxn.result.is_fraud ? 'CRITICAL RISK' : 'SECURE'}
                  </span>
                </div>
              </div>

              {/* Factors Breakdown */}
              <div className="border border-zinc-800 rounded-xl p-3 bg-zinc-950/70 space-y-2">
                <span className="text-[10px] text-zinc-500 font-bold block uppercase">Forensic Factors</span>
                
                <div className="space-y-1.5">
                  <div>
                    <div className="flex justify-between text-[10px] text-zinc-400 mb-0.5">
                      <span>Graph Chain Risk</span>
                      <span>{Math.round(selectedTxn.result.risk_score * 0.4)}%</span>
                    </div>
                    <div className="h-1 bg-zinc-800 rounded-full overflow-hidden">
                      <div className="h-full bg-blue-500" style={{ width: `${selectedTxn.result.risk_score * 0.4}%` }} />
                    </div>
                  </div>

                  <div>
                    <div className="flex justify-between text-[10px] text-zinc-400 mb-0.5">
                      <span>Velocity Risk</span>
                      <span>{Math.round(selectedTxn.result.risk_score * 0.3)}%</span>
                    </div>
                    <div className="h-1 bg-zinc-800 rounded-full overflow-hidden">
                      <div className="h-full bg-yellow-500" style={{ width: `${selectedTxn.result.risk_score * 0.3}%` }} />
                    </div>
                  </div>

                  <div>
                    <div className="flex justify-between text-[10px] text-zinc-400 mb-0.5">
                      <span>Behavior Entropy</span>
                      <span>{Math.round(selectedTxn.result.risk_score * 0.2)}%</span>
                    </div>
                    <div className="h-1 bg-zinc-800 rounded-full overflow-hidden">
                      <div className="h-full bg-purple-500" style={{ width: `${selectedTxn.result.risk_score * 0.2}%` }} />
                    </div>
                  </div>
                </div>
              </div>

              {/* Explain Text */}
              <div className="border border-zinc-800 rounded-xl p-3 bg-zinc-950/70">
                <span className="text-[10px] text-zinc-500 font-bold block uppercase mb-1.5">Oracle Explain Reasoning</span>
                <p className="text-zinc-300 leading-relaxed text-[11px] font-sans">
                  {selectedTxn.result.is_fraud 
                    ? `High-risk score of ${selectedTxn.result.risk_score}% flags anomalous transfers from account ${selectedTxn.transaction.source_account} mimicking lateral network hops. Action blocked.`
                    : `Transaction from ${selectedTxn.transaction.source_account} to ${selectedTxn.transaction.target_account} shows standard volume, low velocity anomaly, and sits within safe network boundaries.`
                  }
                </p>
              </div>

              {/* Action Buttons Panel */}
              <div className="pt-2 space-y-2.5">
                <span className="text-[10px] text-zinc-500 font-bold block uppercase">Operational Actions</span>
                
                {/* Blockchain seal */}
                <button
                  type="button"
                  onClick={() => handleBlockchainSeal(selectedTxn.transaction.transaction_id)}
                  disabled={sealingId !== null || blockchainSeals.some(s => s.transaction_id === selectedTxn.transaction.transaction_id)}
                  className="w-full bg-zinc-900 hover:bg-zinc-800 disabled:bg-zinc-900 border border-zinc-800 hover:border-zinc-700 disabled:border-zinc-900 disabled:text-zinc-600 text-zinc-300 font-bold py-2 px-3 rounded-lg flex items-center justify-center gap-2 transition"
                >
                  <Lock className="w-4 h-4 text-blue-500" />
                  {blockchainSeals.some(s => s.transaction_id === selectedTxn.transaction.transaction_id) 
                    ? 'Evidence Sealed' 
                    : (sealingId === selectedTxn.transaction.transaction_id ? 'Sealing...' : 'Seal Evidence on Chain')
                  }
                </button>

                {/* Honeypot trigger */}
                <button
                  type="button"
                  onClick={() => handleHoneypotTrigger(selectedTxn.transaction.transaction_id)}
                  className={`w-full border font-bold py-2 px-3 rounded-lg flex items-center justify-center gap-2 transition ${
                    honeypots.includes(selectedTxn.transaction.transaction_id)
                      ? 'bg-red-500/10 border-red-500 text-red-500 hover:bg-red-500/20'
                      : 'bg-zinc-900 hover:bg-zinc-800 border-zinc-800 hover:border-zinc-700 text-zinc-300'
                  }`}
                >
                  <AlertTriangle className="w-4 h-4 text-red-500" />
                  {honeypots.includes(selectedTxn.transaction.transaction_id) 
                    ? 'Release Honeypot Trap' 
                    : 'Activate Honeypot Trap'
                  }
                </button>
              </div>

              {/* Blockchain Seal Logs list */}
              {blockchainSeals.length > 0 && (
                <div className="border border-zinc-800 rounded-xl p-2.5 bg-zinc-950/70 flex-1 overflow-y-auto max-h-[140px]">
                  <span className="text-[10px] text-zinc-500 font-bold block uppercase mb-1.5 flex items-center gap-1">
                    <FileText className="w-3.5 h-3.5" />
                    Ledger Audit Trail
                  </span>
                  <div className="space-y-1 text-[9px] font-mono text-zinc-400">
                    {blockchainSeals.map((seal, i) => (
                      <div key={i} className="flex justify-between border-b border-zinc-900 pb-1">
                        <span>{seal.transaction_id}</span>
                        <span className="text-blue-500">{seal.seal_id}</span>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          )}
        </section>
      </main>

      {/* Footer System Info */}
      <footer className="border-t border-[#27272a] bg-[#18181b]/30 px-6 py-3 flex items-center justify-between text-xs text-zinc-600 mt-auto">
        <span>AegisGraph-Sentinel 2.0 Security Operations Dashboard</span>
        <span>Environment: Production Mode</span>
      </footer>
    </div>
  );
}
