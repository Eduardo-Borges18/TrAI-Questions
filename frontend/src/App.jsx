import React, { useState } from 'react';
import axios from 'axios';
import HomePage from './pages/HomePage';
import ExamPage from './pages/ExamPage';
import './index.css';

const API_BASE = 'http://127.0.0.1:8000/api';

function App() {
  const [view, setView] = useState('home'); // 'home' | 'exam'
  const [selectedExam, setSelectedExam] = useState(null);
  const [loadingExam, setLoadingExam] = useState(false);

  const handleSelectExam = async (examSummary) => {
    setLoadingExam(true);
    try {
      const res = await axios.get(`${API_BASE}/exams/${examSummary.id}/`);
      setSelectedExam(res.data);
      setView('exam');
    } catch {
      alert('Não foi possível carregar a prova. Tente novamente.');
    } finally {
      setLoadingExam(false);
    }
  };

  const handleBack = () => {
    setView('home');
    setSelectedExam(null);
  };

  return (
    <div className="app-container">
      <header className="app-header">
        <button className="app-logo-btn" onClick={handleBack} id="btn-logo-home">
          TrAI Questions
        </button>
      </header>

      <main style={{ flex: 1 }}>
        {loadingExam && (
          <div className="card" style={{ textAlign: 'center', padding: '3rem' }}>
            <div className="spinner" style={{ margin: '0 auto', borderTopColor: 'var(--primary)' }} />
            <p style={{ marginTop: '1rem', color: 'var(--text-muted)' }}>Carregando prova...</p>
          </div>
        )}
        {!loadingExam && view === 'home' && (
          <HomePage onSelectExam={handleSelectExam} />
        )}
        {!loadingExam && view === 'exam' && selectedExam && (
          <ExamPage exam={selectedExam} onBack={handleBack} />
        )}
      </main>

      <footer className="app-footer">
        <p>TrAI Questions © {new Date().getFullYear()} — Feedback gerado por IA</p>
      </footer>
    </div>
  );
}

export default App;
