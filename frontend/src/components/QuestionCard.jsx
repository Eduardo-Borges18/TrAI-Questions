import React from 'react';

const DIFFICULTY_COLORS = {
  facil: { bg: '#ECFDF5', text: '#065F46', border: '#A7F3D0', label: 'Fácil' },
  medio: { bg: '#FFFBEB', text: '#92400E', border: '#FDE68A', label: 'Médio' },
  dificil: { bg: '#FEF2F2', text: '#991B1B', border: '#FCA5A5', label: 'Difícil' },
};

const TYPE_ICONS = {
  multipla_escolha: '📋',
  dissertativa: '✍️',
  fechada: '✅',
};

const QuestionCard = ({ question, onClick }) => {
  const diff = DIFFICULTY_COLORS[question.difficulty] || DIFFICULTY_COLORS.medio;
  const icon = TYPE_ICONS[question.question_type] || '❓';

  return (
    <button className="q-card" onClick={() => onClick(question)} id={`question-card-${question.id}`}>
      <div className="q-card__top">
        <span className="q-card__icon">{icon}</span>
        <span
          className="q-card__badge"
          style={{ background: diff.bg, color: diff.text, border: `1px solid ${diff.border}` }}
        >
          {diff.label}
        </span>
      </div>

      <h3 className="q-card__title">{question.title}</h3>
      <p className="q-card__statement">{question.statement}</p>

      <div className="q-card__footer">
        {question.habilidade && (
          <span className="q-card__habilidade" title={question.habilidade.description}>
            🎯 {question.habilidade.code}
          </span>
        )}
        <span className="q-card__type">{question.question_type_label}</span>
      </div>
    </button>
  );
};

export default QuestionCard;
