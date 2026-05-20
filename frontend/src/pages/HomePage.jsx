import React, { useState, useEffect } from 'react';
import axios from 'axios';
import ExamCard from '../components/ExamCard';

const API_BASE = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000/api';

const HomePage = ({ onSelectExam }) => {
  const [exams, setExams] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    axios.get(`${API_BASE}/exams/`)
      .then(r => setExams(r.data))
      .catch(() => setError('Não foi possível conectar ao servidor.'))
      .finally(() => setLoading(false));
  }, []);

  return (
    <div className="home-page">
      <div className="home-hero">
        <div className="home-hero__badge">✨ Powered by AI</div>
        <h1 className="app-logo">TrAI Questions</h1>
        <p className="app-subtitle">
          Escolha uma prova, responda as questões e receba<br />
          avaliação instantânea com feedback da IA.
        </p>
      </div>

      <div className="section-header">
        <h2 className="section-title">📝 Provas Disponíveis</h2>
        {exams.length > 0 && <span className="section-count">{exams.length}</span>}
      </div>

      {loading && (
        <div className="card" style={{ textAlign:'center', padding:'3rem' }}>
          <div className="spinner" style={{ margin:'0 auto', borderTopColor:'var(--primary)' }} />
          <p style={{ marginTop:'1rem', color:'var(--text-muted)' }}>Carregando provas...</p>
        </div>
      )}

      {error && (
        <div className="card error-card">
          <p className="error-text" style={{ marginTop:0 }}>{error}</p>
        </div>
      )}

      {!loading && !error && exams.length === 0 && (
        <div className="empty-state">
          <span>📭</span>
          <h3>Nenhuma prova disponível ainda.</h3>
          <p>O professor pode criar provas em <strong>/admin</strong>.</p>
        </div>
      )}

      {!loading && !error && exams.length > 0 && (
        <div className="cards-grid">
          {exams.map(e => (
            <ExamCard key={e.id} exam={e} onClick={onSelectExam} />
          ))}
        </div>
      )}
    </div>
  );
};

export default HomePage;
