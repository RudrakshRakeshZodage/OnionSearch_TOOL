import { ExternalLink, Tag, Shield, Image as ImageIcon, Mail, FileText, ChevronDown, ChevronUp } from 'lucide-react'
import { useState } from 'react'

const ResultCard = ({ result, index }) => {
  const [expanded, setExpanded] = useState(false)

  // Highlight matched keywords in text
  const highlightText = (text, keywords) => {
    if (!keywords || keywords.length === 0) return text
    const regex = new RegExp(`(${keywords.map(k => k.replace(/[-\/\\^$*+?.()|[\]{}]/g, '\\$&')).join('|')})`, 'gi')
    const parts = text.split(regex)
    return parts.map((part, i) => 
      regex.test(part) ? <mark key={i}>{part}</mark> : part
    )
  }

  return (
    <div className="glass glass-card animate-fade-in" style={{ animationDelay: `${index * 0.1}s` }}>
      <div className="card-header">
        <div className="score-badge">
          <span className="score-label">MATCH SCORE</span>
          <span className="score-value">{result.score.toFixed(1)}%</span>
        </div>
        <div className="card-title">
          <h4>{result.title}</h4>
          <a href={result.url} target="_blank" rel="noopener noreferrer" className="onion-link">
            {result.url} <ExternalLink size={14} />
          </a>
        </div>
      </div>

      <div className="card-body">
        <p className="snippet">
          {highlightText(result.snippet, result.matched_keywords)}
        </p>

        {result.matched_keywords && result.matched_keywords.length > 0 && (
          <div className="matched-tags">
            {result.matched_keywords.map(kw => (
              <span key={kw} className="match-tag">
                <Tag size={12} /> {kw}
              </span>
            ))}
          </div>
        )}

        <div className="metadata-summary">
          {result.emails?.length > 0 && (
            <span className="meta-info">
              <Mail size={14} /> {result.emails.length} Emails
            </span>
          )}
          {result.images?.length > 0 && (
            <span className="meta-info">
              <ImageIcon size={14} /> {result.images.length} Images
            </span>
          )}
        </div>

        {expanded && (
          <div className="expanded-content animate-fade-in">
             {result.images?.length > 0 && (
               <div className="image-gallery">
                 <h5>Extracted Images</h5>
                 <div className="image-grid">
                   {result.images.map((img, i) => (
                     <div key={i} className="image-wrapper">
                       <img src={img} alt="Extracted" onError={(e) => e.target.style.display='none'} />
                     </div>
                   ))}
                 </div>
               </div>
             )}
             
             <div className="meta-details">
               <h5>Technical Details</h5>
               <ul>
                 {Object.entries(result.metadata || {}).map(([key, val]) => (
                   <li key={key}><strong>{key}:</strong> {val}</li>
                 ))}
               </ul>
             </div>
          </div>
        )}
      </div>

      <div className="card-footer">
        <button className="expand-btn" onClick={() => setExpanded(!expanded)}>
          {expanded ? <><ChevronUp size={16} /> Show Less</> : <><ChevronDown size={16} /> Full Intelligence Report</>}
        </button>
        <div className="trust-score">
          <Shield size={14} /> VERIFIED INTEL
        </div>
      </div>

      <style jsx="true">{`
        .card-header {
          display: flex;
          gap: 1.5rem;
          margin-bottom: 1.5rem;
          align-items: flex-start;
        }

        .score-badge {
          background: rgba(0, 210, 255, 0.1);
          border: 1px solid var(--accent-primary);
          padding: 0.5rem;
          border-radius: 12px;
          display: flex;
          flex-direction: column;
          align-items: center;
          min-width: 80px;
        }

        .score-label {
          font-size: 0.65rem;
          font-weight: 700;
          color: var(--accent-primary);
        }

        .score-value {
          font-size: 1.25rem;
          font-weight: 800;
        }

        .card-title h4 {
          font-size: 1.25rem;
          font-weight: 600;
          margin-bottom: 0.25rem;
          color: white;
        }

        .onion-link {
          color: var(--accent-primary);
          font-size: 0.85rem;
          text-decoration: none;
          display: flex;
          align-items: center;
          gap: 0.4rem;
          opacity: 0.8;
          word-break: break-all;
        }

        .card-body {
          margin-bottom: 1.5rem;
        }

        .snippet {
          color: var(--text-secondary);
          line-height: 1.6;
          margin-bottom: 1.25rem;
          font-size: 0.95rem;
        }

        mark {
          background: rgba(0, 210, 255, 0.3);
          color: white;
          border-radius: 2px;
          padding: 0 4px;
        }

        .matched-tags {
          display: flex;
          flex-wrap: wrap;
          gap: 0.5rem;
          margin-bottom: 1.25rem;
        }

        .match-tag {
          font-size: 0.75rem;
          background: rgba(255, 255, 255, 0.05);
          padding: 0.3rem 0.6rem;
          border-radius: 4px;
          display: flex;
          align-items: center;
          gap: 0.4rem;
          color: var(--text-secondary);
        }

        .metadata-summary {
          display: flex;
          gap: 1rem;
          font-size: 0.8rem;
          color: var(--text-secondary);
        }

        .meta-info {
          display: flex;
          align-items: center;
          gap: 0.4rem;
        }

        .card-footer {
          display: flex;
          justify-content: space-between;
          align-items: center;
          padding-top: 1rem;
          border-top: 1px solid var(--border-color);
        }

        .expand-btn {
          background: none;
          border: none;
          color: var(--accent-primary);
          cursor: pointer;
          font-family: inherit;
          display: flex;
          align-items: center;
          gap: 0.5rem;
          font-weight: 600;
          font-size: 0.9rem;
        }

        .trust-score {
          font-size: 0.75rem;
          color: rgba(0, 255, 127, 0.6);
          display: flex;
          align-items: center;
          gap: 0.4rem;
          font-weight: 700;
        }

        /* Expanded content */
        .expanded-content {
          margin-top: 1.5rem;
          padding-top: 1.5rem;
          border-top: 1px dashed var(--border-color);
        }

        h5 {
          font-size: 0.9rem;
          font-weight: 700;
          margin-bottom: 1rem;
          color: var(--accent-primary);
          text-transform: uppercase;
          letter-spacing: 0.05em;
        }

        .image-grid {
          display: grid;
          grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
          gap: 0.75rem;
          margin-bottom: 1.5rem;
        }

        .image-wrapper {
          aspect-ratio: 1;
          background: #1a1b23;
          border-radius: 8px;
          overflow: hidden;
          border: 1px solid var(--border-color);
        }

        .image-wrapper img {
          width: 100%;
          height: 100%;
          object-fit: cover;
          transition: transform 0.3s;
        }

        .image-wrapper:hover img {
          transform: scale(1.1);
        }

        .meta-details ul {
          list-style: none;
          font-size: 0.85rem;
          color: var(--text-secondary);
        }

        .meta-details li {
          margin-bottom: 0.4rem;
          padding-bottom: 0.4rem;
          border-bottom: 1px solid rgba(255, 255, 255, 0.02);
        }
      `}</style>
    </div>
  )
}

export default ResultCard
