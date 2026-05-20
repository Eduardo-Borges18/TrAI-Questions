import React, { useState } from 'react';
import axios from 'axios';

const API_BASE = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000/api';

const getScoreClass = (score) => {
  if (score >= 7) return 'score-high';
  if (score >= 4) return 'score-mid';
  return 'score-low';
};

const QuestionPage = ({ question, examId = null, onBack, onNext = null, examProgress = null }) => {
  const [answer, setAnswer] = useState('');
  const [selectedAlt, setSelectedAlt] = useState(null);
  const [pageStatus, setPageStatus] = useState('idle'); // idle | loading | success | error
  const [feedback, setFeedback] = useState(null);
  const [errorMsg, setErrorMsg] = useState('');

  const isMultipleChoice = question.question_type === 'fechada';
  const hasAlternatives = question.alternatives && question.alternatives.length > 0;

  const handleSubmit = async (e) => {
    e.preventDefault();
    const answerToSend = isMultipleChoice && hasAlternatives
      ? (selectedAlt ? `Alternativa ${selectedAlt.letter}: ${selectedAlt.text}` : '')
      : answer;

    if (!answerToSend.trim()) return;

    setPageStatus('loading');
    setErrorMsg('');

    try {
      const payload = {
        question_id: question.id,
        answer_text: answerToSend,
      };
      if (examId) payload.exam_id = examId;

      const response = await axios.post(`${API_BASE}/submissions/`, payload);
      setFeedback(response.data);
      setPageStatus('success');
    } catch (err) {
      console.error(err);
      const serverMsg = err.response?.data?.error;
      setErrorMsg(serverMsg || 'Ocorreu um erro ao processar. Tente novamente.');
      setPageStatus('error');
    }
  };

  const handleReset = () => {
    setAnswer('');
    setSelectedAlt(null);
    setFeedback(null);
    setErrorMsg('');
    setPageStatus('idle');
  };

  return (
    <div className="question-page">
      {/* Barra de progresso da prova */}
      {examProgress && (
        <div className="exam-progress-bar">
          <div className="exam-progress-bar__info">
            <span>Questão {examProgress.current} de {examProgress.total}</span>
            <span>{Math.round((examProgress.current / examProgress.total) * 100)}%</span>
          </div>
          <div className="exam-progress-bar__track">
            <div
              className="exam-progress-bar__fill"
              style={{ width: `${(examProgress.current / examProgress.total) * 100}%` }}
            />
          </div>
        </div>
      )}

      {/* Botão voltar */}
      <button className="back-btn" onClick={onBack} id="btn-back">
        ← {examProgress ? 'Abandonar Prova' : 'Voltar'}
      </button>

      <div className="card">
        {/* Cabeçalho da questão */}
        <div className="header">
          <div className="question-meta-row">
            {question.habilidade && (
              <span className="meta-tag meta-tag--blue" title={question.habilidade.description}>
                🎯 {question.habilidade.code}
              </span>
            )}
            <span className="meta-tag meta-tag--gray">{question.difficulty_label}</span>
            <span className="meta-tag meta-tag--gray">{question.question_type_label}</span>
          </div>
          <h2 className="question-title">{question.title}</h2>
          <p className="question-desc">{question.statement}</p>
        </div>

        {/* Formulário de resposta */}
        {pageStatus !== 'success' && (
          <form onSubmit={handleSubmit} className="form-group">
            {isMultipleChoice && hasAlternatives ? (
              /* Alternativas */
              <div className="alternatives-list">
                {question.alternatives.map((alt) => (
                  <button
                    key={alt.id}
                    type="button"
                    className={`alternative-btn ${selectedAlt?.id === alt.id ? 'alternative-btn--selected' : ''}`}
                    onClick={() => setSelectedAlt(alt)}
                    disabled={pageStatus === 'loading'}
                  >
                    <span className="alternative-btn__letter">{alt.letter}</span>
                    <span className="alternative-btn__text">{alt.text}</span>
                  </button>
                ))}
              </div>
            ) : (
              /* Dissertativa / Fechada */
              <textarea
                id="answer-input"
                className="textarea-input"
                placeholder="Desenvolva sua resposta aqui com detalhes..."
                value={answer}
                onChange={(e) => setAnswer(e.target.value)}
                disabled={pageStatus === 'loading'}
              />
            )}

            <button
              type="submit"
              disabled={
                pageStatus === 'loading' ||
                (isMultipleChoice && hasAlternatives ? !selectedAlt : !answer.trim())
              }
              className="submit-btn"
              id="btn-submit-answer"
            >
              {pageStatus === 'loading' ? (
                <>
                  <div className="spinner" aria-hidden="true" />
                  <span>Analisando com IA...</span>
                </>
              ) : 'Enviar Resposta'}
            </button>

            {pageStatus === 'error' && (
              <p className="error-text" role="alert">{errorMsg}</p>
            )}
          </form>
        )}

        {/* Feedback */}
        {pageStatus === 'success' && feedback && (
          <div className="feedback-container">
            <div className="score-display">
              <span className={`score-badge ${getScoreClass(feedback.score)}`}>
                {Number(feedback.score).toFixed(1)}
              </span>
              <span className="score-label">/ 10</span>
            </div>

            <h3 className="feedback-title">Análise da Resposta</h3>

            <div className="feedback-box main">
              <h4>💬 Feedback do Professor IA</h4>
              <p>{feedback.constructive_feedback}</p>
            </div>

            <div className="feedback-grid">
              <div className="insight-card strengths">
                <h4><span className="icon">🚀</span> Pontos Fortes</h4>
                <p>{feedback.key_strengths}</p>
              </div>
              <div className="insight-card improvements">
                <h4><span className="icon">🎯</span> Pontos a Melhorar</h4>
                <p>{feedback.areas_for_improvement}</p>
              </div>
            </div>

            {/* Botões de ação */}
            <div className="feedback-actions">
              {onNext ? (
                <button className="submit-btn" onClick={() => onNext(feedback)} id="btn-next-question">
                  Próxima Questão →
                </button>
              ) : (
                <button className="reset-link" onClick={handleReset}>
                  ↺ Responder novamente
                </button>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default QuestionPage;
