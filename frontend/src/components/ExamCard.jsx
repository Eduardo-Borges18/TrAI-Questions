import React from 'react';

const DIFFICULTY_COLORS = {
  facil: { bg: '#ECFDF5', text: '#065F46', border: '#A7F3D0', label: 'Fácil' },
  medio: { bg: '#FFFBEB', text: '#92400E', border: '#FDE68A', label: 'Médio' },
  dificil: { bg: '#FEF2F2', text: '#991B1B', border: '#FCA5A5', label: 'Difícil' },
};

const ExamCard = ({ exam, onClick }) => {
  const diff = DIFFICULTY_COLORS[exam.difficulty_level] || DIFFICULTY_COLORS.medio;
  const totalQ = exam.total_questions || exam.question_count;

  return (
    <button className="exam-card" onClick={() => onClick(exam)} id={`exam-card-${exam.id}`}>
      <div className="exam-card__header">
        <span className="exam-card__icon">📝</span>
        <span
          className="exam-card__badge"
          style={{ background: diff.bg, color: diff.text, border: `1px solid ${diff.border}` }}
        >
          {diff.label}
        </span>
      </div>

      <h3 className="exam-card__title">{exam.title}</h3>
      {exam.description && <p className="exam-card__desc">{exam.description}</p>}

      <div className="exam-card__meta">
        <div className="exam-card__meta-item">
          <span className="exam-card__meta-icon">❓</span>
          <span>{totalQ} {totalQ === 1 ? 'questão' : 'questões'}</span>
        </div>
        <div className="exam-card__meta-item">
          <span className="exam-card__meta-icon">📂</span>
          <span>{exam.question_type_label}</span>
        </div>
        {exam.themes && (
          <div className="exam-card__meta-item">
            <span className="exam-card__meta-icon">🏷️</span>
            <span>{exam.themes}</span>
          </div>
        )}
      </div>

      <div className="exam-card__cta">
        Iniciar Prova →
      </div>
    </button>
  );
};

export default ExamCard;
