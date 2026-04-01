import { useState } from 'react'
import { Plus, X, Search, Terminal } from 'lucide-react'

const SearchForm = ({ onSearch, loading }) => {
  const [primary, setPrimary] = useState('')
  const [secondary, setSecondary] = useState('')
  const [tags, setTags] = useState([])
  const [amount, setAmount] = useState(20)

  const addTag = (e) => {
    if (e) e.preventDefault()
    if (secondary && !tags.includes(secondary)) {
      setTags([...tags, secondary])
      setSecondary('')
    }
  }

  const removeTag = (tag) => {
    setTags(tags.filter(t => t !== tag))
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    if (!primary) return
    onSearch({
      primary_keyword: primary,
      secondary_keywords: tags,
      amount: parseInt(amount),
      include_images: true
    })
  }

  return (
    <form className="search-form glass animate-fade-in" onSubmit={handleSubmit}>
      <div className="input-group main-input">
        <Search className="input-icon" size={20} />
        <input 
          type="text" 
          placeholder="Enter primary organization or keyword (e.g. PayPal)"
          value={primary}
          onChange={(e) => setPrimary(e.target.value)}
          required
        />
      </div>

      <div className="input-group secondary-input">
        <Terminal className="input-icon" size={18} />
        <input 
          type="text" 
          placeholder="Add leak vectors (e.g. credentials, email, database)"
          value={secondary}
          onChange={(e) => setSecondary(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && addTag(e)}
        />
        <button type="button" className="add-btn" onClick={addTag}>
          <Plus size={18} />
        </button>
      </div>

      {tags.length > 0 && (
        <div className="tags-container">
          {tags.map(tag => (
            <span key={tag} className="tag animate-fade-in">
              {tag}
              <X size={14} className="remove-tag" onClick={() => removeTag(tag)} />
            </span>
          ))}
        </div>
      )}

      <div className="form-footer">
        <div className="amount-selector">
          <label>Results Limit:</label>
          <select value={amount} onChange={(e) => setAmount(e.target.value)}>
            <option value="10">10</option>
            <option value="20">20</option>
            <option value="50">50</option>
            <option value="100">100</option>
          </select>
        </div>
        <button type="submit" className="submit-btn" disabled={loading || !primary}>
          {loading ? 'Searching...' : 'Initiate Intel Scan'}
        </button>
      </div>

      <style jsx="true">{`
        .search-form {
          max-width: 800px;
          margin: 0 auto;
          padding: 2rem;
          display: flex;
          flex-direction: column;
          gap: 1.5rem;
          box-shadow: 0 20px 40px rgba(0,0,0,0.4);
        }

        .input-group {
          position: relative;
          display: flex;
          align-items: center;
          background: rgba(255, 255, 255, 0.05);
          border: 1px solid var(--border-color);
          border-radius: 12px;
          padding: 0.5rem 1rem;
          transition: all 0.3s ease;
        }

        .input-group:focus-within {
          border-color: var(--accent-primary);
          background: rgba(255, 255, 255, 0.08);
          box-shadow: 0 0 15px rgba(0, 210, 255, 0.2);
        }

        .input-icon {
          color: var(--text-secondary);
          margin-right: 1rem;
        }

        input {
          background: none;
          border: none;
          color: white;
          font-family: inherit;
          font-size: 1.1rem;
          width: 100%;
          outline: none;
          padding: 0.5rem 0;
        }

        .add-btn {
          background: var(--accent-primary);
          border: none;
          color: black;
          border-radius: 6px;
          padding: 0.4rem;
          cursor: pointer;
          transition: transform 0.2s;
        }

        .add-btn:hover {
          transform: scale(1.1);
        }

        .tags-container {
          display: flex;
          flex-wrap: wrap;
          gap: 0.5rem;
        }

        .tag {
          background: rgba(0, 210, 255, 0.15);
          color: var(--accent-primary);
          padding: 0.4rem 0.8rem;
          border-radius: 6px;
          font-size: 0.9rem;
          font-weight: 600;
          display: flex;
          align-items: center;
          gap: 0.5rem;
          border: 1px solid rgba(0, 210, 255, 0.3);
        }

        .remove-tag {
          cursor: pointer;
          opacity: 0.7;
        }

        .remove-tag:hover {
          opacity: 1;
        }

        .form-footer {
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin-top: 1rem;
        }

        .amount-selector {
          display: flex;
          align-items: center;
          gap: 1rem;
          color: var(--text-secondary);
        }

        select {
          background: #1a1b23;
          color: white;
          border: 1px solid var(--border-color);
          padding: 0.4rem 0.8rem;
          border-radius: 6px;
          outline: none;
        }

        .submit-btn {
          background: linear-gradient(135deg, var(--accent-primary), #0072ff);
          color: white;
          border: none;
          padding: 0.8rem 2rem;
          border-radius: 12px;
          font-size: 1.1rem;
          font-weight: 700;
          cursor: pointer;
          transition: all 0.3s ease;
          letter-spacing: 0.02em;
        }

        .submit-btn:hover:not(:disabled) {
          transform: translateY(-2px);
          box-shadow: 0 10px 20px rgba(0, 210, 255, 0.3);
        }

        .submit-btn:disabled {
          opacity: 0.5;
          cursor: not-allowed;
        }
      `}</style>
    </form>
  )
}

export default SearchForm
