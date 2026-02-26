import React, { useState, useEffect } from 'react'
import { supabase } from './supabase'
import './index.css'
import logoUrl from './assets/logo.png'

function App() {
  const [articles, setArticles] = useState([]);

  const [viewMode, setViewMode] = useState('feed'); // 'feed' or 'saved'
  const [searchQuery, setSearchQuery] = useState('');
  const [searchHistory, setSearchHistory] = useState(() => {
    const saved = localStorage.getItem('searchHistory');
    return saved ? JSON.parse(saved) : [];
  });
  const [showSuggestions, setShowSuggestions] = useState(false);
  useEffect(() => {
    // Fetch live data from Supabase
    const fetchArticles = async () => {
      try {
        const { data, error } = await supabase
          .from('articles')
          .select('*')
          .order('published_at', { ascending: false });

        if (error) {
          console.error("Failed to load articles from Supabase", error);
        } else if (data) {
          setArticles(data);
        }
      } catch (err) {
        console.error("Error fetching data:", err);
      }
    };

    fetchArticles();
  }, []);

  const toggleSave = async (id, currentState) => {
    const newState = !currentState;

    // Optimistic UI update
    setArticles(articles.map(article =>
      article.id === id ? { ...article, is_saved: newState } : article
    ));

    // Update Supabase
    const { error } = await supabase
      .from('articles')
      .update({ is_saved: newState })
      .eq('id', id);

    if (error) {
      console.error("Error saving article:", error);
      // Revert UI on failure
      setArticles(articles.map(article =>
        article.id === id ? { ...article, is_saved: currentState } : article
      ));
    }
  };

  const handleSearchSubmit = (e) => {
    e.preventDefault();
    if (searchQuery.trim() && !searchHistory.includes(searchQuery.trim())) {
      const newHistory = [searchQuery.trim(), ...searchHistory].slice(0, 5);
      setSearchHistory(newHistory);
      localStorage.setItem('searchHistory', JSON.stringify(newHistory));
    }
    setShowSuggestions(false);
  };

  const displayedArticles = (viewMode === 'feed' ? articles : articles.filter(a => a.is_saved))
    .filter(a =>
      a.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      a.summary.toLowerCase().includes(searchQuery.toLowerCase())
    );

  return (
    <div className="dashboard-container">
      <header className="header">
        <div className="logo"><img src={logoUrl} alt="NewsFeed Logo" /></div>

        <div className="search-container">
          <form onSubmit={handleSearchSubmit} className="search-form">
            <input
              type="text"
              placeholder="Search articles..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              onFocus={() => setShowSuggestions(true)}
              onBlur={() => setTimeout(() => setShowSuggestions(false), 200)}
              className="search-input"
            />
            <button type="submit" className="search-icon-btn">🔍</button>
          </form>
          {showSuggestions && searchHistory.length > 0 && (
            <ul className="search-suggestions">
              <li className="suggestions-header">Recent Searches</li>
              {searchHistory.map((item, index) => (
                <li
                  key={index}
                  className="suggestion-item"
                  onMouseDown={(e) => {
                    e.preventDefault(); // Prevent blur
                    setSearchQuery(item);
                    setShowSuggestions(false);
                  }}
                >
                  <span className="history-icon">🕒</span> {item}
                </li>
              ))}
            </ul>
          )}
        </div>

        <div className="tab-container">
          <button
            className={`tab-btn ${viewMode === 'feed' ? 'active' : ''}`}
            onClick={() => setViewMode('feed')}
          >
            New Feed
          </button>
          <button
            className={`tab-btn ${viewMode === 'saved' ? 'active' : ''}`}
            onClick={() => setViewMode('saved')}
          >
            Saved Articles
          </button>
        </div>
        <button className="primary-btn">Sync Data</button>
      </header>

      <main>
        {displayedArticles.length === 0 ? (
          <div className="empty-state">
            <p>No articles found for this view.</p>
          </div>
        ) : (
          <div className="article-grid">
            {displayedArticles.map(article => (
              <article key={article.id} className="article-card">
                <span className="article-source">{article.source}</span>
                <h3 className="article-title">{article.title}</h3>
                <p className="article-summary">{article.summary}</p>

                <div className="article-footer">
                  <a href={article.url} target="_blank" rel="noreferrer" className="read-more">Read Full &rarr;</a>
                  <button
                    className={`save-btn ${article.is_saved ? 'saved' : ''}`}
                    onClick={() => toggleSave(article.id, article.is_saved)}
                    aria-label="Save Article"
                  >
                    {article.is_saved ? '♥' : '♡'}
                  </button>
                </div>
              </article>
            ))}
          </div>
        )}
      </main>
    </div>
  )
}

export default App
