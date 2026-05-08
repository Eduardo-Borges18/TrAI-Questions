import React, { useState } from 'react';
import QuestionPage from './QuestionPage';

const getScoreClass = (score) => {
  if (score >= 7) return 'score-high';
  if (score >= 4) return 'score-mid';
  return 'score-low';
};

const ExamPage = ({ exam, onBack }) => {
  const questions = exam.questions || [];
  const [currentIndex, setCurrentIndex] = useState(0);
  const [results, setResults] = useState([]); // { question, feedback }
  const [examDone, setExamDone] = useState(false);

  const currentQuestion = questions[currentIndex];

  const handleNext = (feedback) => {
    if (feedback) {
      setResults(prev => [...prev, { title: currentQuestion.statement.substring(0, 40) + '...', score: feedback.score }]);
    }
    if (currentIndex + 1 < questions.length) {
      setCurrentIndex((i) => i + 1);
    } else {
      setExamDone(true);
    }
  };

  // Captura feedback ao enviar — QuestionPage chama onNext, mas precisamos capturar o resultado
  // Por isso usamos um wrapper que escuta o evento de feedback via window event
  // ou simplesmente avançamos e mostramos resumo ao final

  if (questions.length === 0) {
    return (
      <div className="question-page">
        <button className="back-btn" onClick={onBack}>← Voltar</button>
        <div className="card" style={{ textAlign: 'center', padding: '3rem' }}>
          <p style={{ fontSize: '3rem' }}>📭</p>
          <h3 style={{ marginTop: '1rem' }}>Esta prova ainda não tem questões cadastradas.</h3>
          <p style={{ color: 'var(--text-muted)', marginTop: '0.5rem' }}>
            O professor precisa adicionar questões no painel admin.
          </p>
        </div>
      </div>
    );
  }

  // Tela de resumo final
  if (examDone) {
    const avg = results.length
      ? results.reduce((sum, r) => sum + Number(r.score || 0), 0) / results.length
      : 0;

    return (
      <div className="question-page">
        <button className="back-btn" onClick={onBack} id="btn-back-from-summary">← Voltar ao Início</button>
        <div className="card">
          <div style={{ textAlign: 'center', marginBottom: '2rem' }}>
            <span style={{ fontSize: '3rem' }}>🎉</span>
            <h2 style={{ marginTop: '0.5rem', fontWeight: 800 }}>Prova Concluída!</h2>
            <p style={{ color: 'var(--text-muted)', marginTop: '0.25rem' }}>{exam.title}</p>
          </div>

          {/* Média geral */}
          <div className="score-display" style={{ marginBottom: '2rem' }}>
            <span className={`score-badge ${getScoreClass(avg)}`}>
              {avg.toFixed(1)}
            </span>
            <span className="score-label">/ 10 — média final</span>
          </div>

          {/* Tabela de resultados */}
          {results.length > 0 && (
            <div className="exam-results-table">
              <h3 style={{ fontWeight: 700, marginBottom: '1rem' }}>Resumo por Questão</h3>
              {results.map((r, i) => (
                <div key={i} className="exam-result-row">
                  <div className="exam-result-row__info">
                    <span className="exam-result-row__num">Q{i + 1}</span>
                    <span className="exam-result-row__title">{r.title}</span>
                  </div>
                  <span className={`score-badge score-badge--sm ${getScoreClass(r.score)}`}>
                    {Number(r.score).toFixed(1)}
                  </span>
                </div>
              ))}
            </div>
          )}

          <button className="submit-btn" style={{ marginTop: '2rem', width: '100%', justifyContent: 'center' }} onClick={onBack} id="btn-finish-exam">
            Voltar ao Início
          </button>
        </div>
      </div>
    );
  }

  return (
    <QuestionPage
      key={currentQuestion.id}
      question={currentQuestion}
      examId={exam.id}
      onBack={onBack}
      onNext={handleNext}
      examProgress={{ current: currentIndex + 1, total: questions.length }}
    />
  );
};

export default ExamPage;
