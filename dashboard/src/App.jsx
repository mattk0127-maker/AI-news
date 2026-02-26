import React, { useState, useEffect } from 'react'
import { supabase } from './supabase'
import './index.css'

function App() {
  const [articles, setArticles] = useState([]);

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

  return (
    <div className="dashboard-container">
      <header className="header">
        <div className="logo">NewsFeed.</div>
        <button className="primary-btn">Sync Data</button>
      </header>

      <main>
        <div className="article-grid">
          {articles.map(article => (
            <article key={article.id} className="article-card">
              <span className="article-source">{article.source}</span>
              <h3 className="article-title">{article.title}</h3>
              <p className="article-summary">{article.summary}</p>

              <div className="article-footer">
                <a href={article.url} className="read-more">Read Full &rarr;</a>
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
      </main>
    </div>
  )
}

export default App
