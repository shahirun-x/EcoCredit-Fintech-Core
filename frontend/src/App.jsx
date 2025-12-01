import { useState } from 'react'
import axios from 'axios'

function App() {
  const [description, setDescription] = useState("STARBUCKS COFFEE")
  const [amount, setAmount] = useState(8.50)
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)

  const analyzeTransaction = async () => {
    setLoading(true);
    setResult(null);
    try {
      const BACKEND_URL = "https://ominous-space-chainsaw-974j77g95q76cxj7w-8000.app.github.dev"; // <--- Paste here, NO trailing slash

const response = await axios.post(`${BACKEND_URL}/api/v1/analyze`, {
  description: description,
  amount: parseFloat(amount),
  currency: "USD"
});
      setResult(response.data);
    } catch (error) {
      console.error("Error analyzing:", error);
      alert("System Offline. Check Backend Connection.");
    }
    setLoading(false);
  }

  return (
    <div className="min-h-screen flex flex-col items-center justify-center p-4 font-sans bg-eco-bg">
      
      {/* Status Bar */}
      <div className="absolute top-4 right-4 flex items-center space-x-2">
        <span className="relative flex h-3 w-3">
          <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-eco-accent opacity-75"></span>
          <span className="relative inline-flex rounded-full h-3 w-3 bg-eco-accent"></span>
        </span>
        <span className="text-xs text-eco-dim font-mono">SYSTEM OPERATIONAL</span>
      </div>

      {/* Main Card */}
      <div className="w-full max-w-md bg-eco-card rounded-xl shadow-2xl overflow-hidden border border-emerald-800">
        
        {/* Header */}
        <div className="bg-emerald-900/50 p-6 border-b border-emerald-800">
          <h1 className="text-2xl font-bold text-eco-text tracking-wider">EcoCredit<span className="text-eco-accent">.ai</span></h1>
          <p className="text-eco-dim text-xs font-mono uppercase tracking-widest mt-1">Enterprise Risk Engine v1.0</p>
        </div>

        {/* Input Section */}
        <div className="p-6 space-y-5">
          <div>
            <label className="block text-xs font-bold text-eco-dim uppercase mb-2 tracking-wider">Transaction Descriptor</label>
            <input 
              type="text" 
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              className="w-full bg-emerald-900/30 border border-emerald-700 rounded p-3 text-eco-text focus:ring-2 focus:ring-eco-accent focus:border-transparent outline-none transition-all placeholder-emerald-700"
            />
          </div>

          <div>
            <label className="block text-xs font-bold text-eco-dim uppercase mb-2 tracking-wider">Amount (USD)</label>
            <input 
              type="number" 
              value={amount}
              onChange={(e) => setAmount(e.target.value)}
              className="w-full bg-emerald-900/30 border border-emerald-700 rounded p-3 text-eco-text focus:ring-2 focus:ring-eco-accent focus:border-transparent outline-none transition-all"
            />
          </div>

          <button 
            onClick={analyzeTransaction}
            disabled={loading}
            className="w-full bg-eco-accent hover:bg-emerald-400 text-emerald-900 font-bold py-4 rounded shadow-lg hover:shadow-emerald-500/20 transition-all disabled:opacity-50 disabled:cursor-not-allowed uppercase tracking-wide"
          >
            {loading ? "Processing Data Stream..." : "Run Impact Analysis"}
          </button>
        </div>

        {/* Results Section */}
        {result && (
          <div className="bg-emerald-900/80 p-6 border-t border-emerald-700 backdrop-blur-sm">
            <div className="flex justify-between items-end mb-4 border-b border-emerald-700/50 pb-4">
              <div>
                <p className="text-xs text-eco-dim uppercase">Detected Category</p>
                <p className="text-xl font-bold text-white">{result.category}</p>
              </div>
              <div className="text-right">
                <p className="text-xs text-eco-dim uppercase">Risk Score</p>
                <div className={`text-2xl font-black ${result.green_score > 7 ? 'text-eco-accent' : 'text-red-400'}`}>
                  {result.green_score} <span className="text-sm text-eco-dim font-normal">/ 10</span>
                </div>
              </div>
            </div>

            <div className="bg-emerald-950/50 p-4 rounded border border-emerald-800/50 text-sm text-eco-text leading-relaxed">
              <span className="text-eco-accent font-bold mr-2">›› ANALYSIS:</span>
              {result.reasoning}
            </div>

            <div className="mt-4 flex justify-between items-center text-xs font-mono text-emerald-500/80">
              <span>CO2e: {result.carbon_kg} KG</span>
              <span>ID: {Math.random().toString(36).substr(2, 9).toUpperCase()}</span>
            </div>
          </div>
        )}
      </div>

      <div className="mt-8 text-emerald-900/40 text-xs font-mono">
        SECURED BY 256-BIT ENCRYPTION
      </div>
    </div>
  )
}

export default App