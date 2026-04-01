import { useState, useEffect } from 'react'
import axios from 'axios'
import { Search, History, Shield, AlertTriangle, ChevronRight, ExternalLink, Image as ImageIcon, Filter, Trophy } from 'lucide-react'
import SearchForm from './components/SearchForm'
import ResultCard from './components/ResultCard'
import './App.css'

function App() {
  const [task, setTask] = useState(null)
  const [loading, setLoading] = useState(false)
  const [history, setHistory] = useState([])
  const [view, setView] = useState('search') // 'search' or 'history'
  const [status, setStatus] = useState('')

  const handleSearch = async (searchData) => {
    setLoading(true)
    setTask(null)
    setStatus('Initializing search engine...')
    try {
      const response = await axios.post('/api/search', searchData)
      setTask(response.data)
      pollTask(response.data.id)
    } catch (error) {
      console.error('Search failed:', error)
      setLoading(false)
    }
  }

  const pollTask = (taskId) => {
    setStatus('Crawling indexed services...')
    const interval = setInterval(async () => {
      try {
        const response = await axios.get(`/api/tasks/${taskId}`)
        const updatedTask = response.data
        setTask(updatedTask)
        
        if (updatedTask.status === 'completed' || updatedTask.status === 'failed') {
          clearInterval(interval)
          setLoading(false)
          fetchHistory()
        } else if (updatedTask.status === 'running') {
          setStatus('Scoring matches and extracting metadata...')
        }
      } catch (error) {
        console.error('Polling failed:', error)
        clearInterval(interval)
        setLoading(false)
      }
    }, 2000)
  }

  const fetchHistory = async () => {
    try {
      const response = await axios.get('/api/history')
      setHistory(response.data)
    } catch (error) {
      console.error('Failed to fetch history:', error)
    }
  }

  useEffect(() => {
    fetchHistory()
  }, [])

  return (
    <div className="app-container">
      <header className="glass">
        <div className="logo">
          <Shield className="accent-icon" />
          <h1>DarkWeb<span>Intel</span></h1>
        </div>
        <nav>
          <button 
            className={view === 'search' ? 'active' : ''} 
            onClick={() => setView('search')}
          >
            <Search size={18} /> Search
          </button>
          <button 
            className={view === 'history' ? 'active' : ''} 
            onClick={() => setView('history')}
          >
            <History size={18} /> History
          </button>
        </nav>
      </header>

      <main>
        {view === 'search' ? (
          <div className="search-view">
            <section className="search-header">
              <h2>Intel Discovery Engine</h2>
              <p>Monitor dark web leaks with automated scoring and ranking.</p>
              <SearchForm onSearch={handleSearch} loading={loading} />
            </section>

            {loading && (
              <div className="status-indicator glass animate-fade-in">
                <div className="spinner"></div>
                <span>{status}</span>
              </div>
            )}

            {task && task.results && task.results.length > 0 && (
              <div className="results-section">
                <div className="results-header">
                  <h3>
                    <Trophy className="accent-icon" size={20} /> 
                    Top Relevant Matches ({task.results.length})
                  </h3>
                  <div className="filters">
                    <Filter size={16} /> Filters
                  </div>
                </div>
                <div className="results-grid">
                  {task.results.map((result, index) => (
                    <ResultCard key={index} result={result} index={index} />
                  ))}
                </div>
              </div>
            )}

            {task && task.status === 'completed' && task.results.length === 0 && (
              <div className="empty-state glass">
                <AlertTriangle size={48} className="warning-icon" />
                <h3>No Matches Found</h3>
                <p>Try adjusting your keywords or increasing the search depth.</p>
              </div>
            )}
          </div>
        ) : (
          <div className="history-view">
            <h2>Search History</h2>
            <div className="history-list">
              {history.length > 0 ? history.map((h, i) => (
                <div key={i} className="history-item glass" onClick={() => { setTask(h); setView('search'); }}>
                   <div className="history-info">
                     <strong>Search for: "{h.results?.[0]?.matched_keywords?.[0] || 'Unknown'}"</strong>
                     <span>{h.results?.length || 0} results found</span>
                   </div>
                   <ChevronRight size={20} />
                </div>
              )) : (
                <p>No history available yet.</p>
              )}
            </div>
          </div>
        )}
      </main>

      <footer className="glass">
        <p>&copy; 2026 DarkWebIntel Platform • For Research Purposes Only</p>
        <div className="safety-badge">
          <Shield size={14} /> SECURED ENVIRONMENT
        </div>
      </footer>
    </div>
  )
}

export default App
