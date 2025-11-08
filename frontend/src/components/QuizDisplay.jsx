import React, { useState } from 'react';

const QuizDisplay = ({ quizData }) => {
  const [selectedAnswers, setSelectedAnswers] = useState({});
  const [showResults, setShowResults] = useState(false);

  if (!quizData || !quizData.full_quiz_data) {
    return (
      <div className="text-center text-gray-500 py-8">
        No quiz data available
      </div>
    );
  }

  const { summary, questions } = quizData.full_quiz_data;

  const handleAnswerSelect = (questionIndex, optionIndex) => {
    if (showResults) return;
    setSelectedAnswers({
      ...selectedAnswers,
      [questionIndex]: optionIndex,
    });
  };

  const calculateScore = () => {
    let correct = 0;
    questions.forEach((question, qIndex) => {
      const selectedOptionIndex = selectedAnswers[qIndex];
      if (selectedOptionIndex !== undefined) {
        const selectedOption = question.options[selectedOptionIndex];
        if (selectedOption.is_correct) {
          correct++;
        }
      }
    });
    return { correct, total: questions.length };
  };

  const score = calculateScore();

  const getOptionClass = (questionIndex, optionIndex, option) => {
    if (!showResults) {
      return selectedAnswers[questionIndex] === optionIndex
        ? 'bg-blue-500 text-white border-blue-500'
        : 'bg-white hover:bg-gray-50 border-gray-300';
    }

    // Show results
    if (option.is_correct) {
      return 'bg-green-500 text-white border-green-500';
    }
    if (selectedAnswers[questionIndex] === optionIndex && !option.is_correct) {
      return 'bg-red-500 text-white border-red-500';
    }
    return 'bg-gray-100 text-gray-600 border-gray-300';
  };

  return (
    <div className="space-y-6">
      {/* Summary */}
      <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
        <h3 className="text-lg font-semibold text-blue-900 mb-2">Summary</h3>
        <p className="text-blue-800">{summary}</p>
      </div>

      {/* Questions */}
      <div className="space-y-6">
        {questions.map((question, qIndex) => (
          <div key={qIndex} className="bg-white border border-gray-200 rounded-lg p-6 shadow-sm">
            <h4 className="text-lg font-semibold text-gray-800 mb-4">
              {qIndex + 1}. {question.question}
            </h4>
            
            <div className="space-y-2">
              {question.options.map((option, oIndex) => (
                <button
                  key={oIndex}
                  onClick={() => handleAnswerSelect(qIndex, oIndex)}
                  disabled={showResults}
                  className={`w-full text-left p-3 rounded-lg border-2 transition-all ${getOptionClass(qIndex, oIndex, option)} ${
                    !showResults ? 'cursor-pointer' : 'cursor-default'
                  }`}
                >
                  <span className="font-medium">
                    {String.fromCharCode(65 + oIndex)}. {option.text}
                  </span>
                </button>
              ))}
            </div>

            {showResults && question.explanation && (
              <div className="mt-4 p-3 bg-gray-50 rounded-lg">
                <p className="text-sm text-gray-700">
                  <span className="font-semibold">Explanation:</span> {question.explanation}
                </p>
              </div>
            )}
          </div>
        ))}
      </div>

      {/* Score and Submit Button */}
      <div className="flex justify-between items-center pt-4 border-t">
        <div>
          {showResults && (
            <div className="text-lg font-semibold text-gray-800">
              Score: {score.correct} / {score.total} (
              {Math.round((score.correct / score.total) * 100)}%)
            </div>
          )}
        </div>
        <button
          onClick={() => setShowResults(!showResults)}
          className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors font-semibold"
        >
          {showResults ? 'Hide Results' : 'Show Results'}
        </button>
      </div>
    </div>
  );
};

export default QuizDisplay;

