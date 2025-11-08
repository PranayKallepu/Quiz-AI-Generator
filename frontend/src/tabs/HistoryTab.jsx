import React, { useState, useEffect } from 'react';
import { getHistory, getQuiz } from '../services/api';
import QuizDisplay from '../components/QuizDisplay';
import Modal from '../components/Modal';

const HistoryTab = () => {
  const [quizzes, setQuizzes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [selectedQuiz, setSelectedQuiz] = useState(null);
  const [modalOpen, setModalOpen] = useState(false);
  const [loadingQuiz, setLoadingQuiz] = useState(false);

  useEffect(() => {
    fetchHistory();
  }, []);

  const fetchHistory = async () => {
    setLoading(true);
    setError('');
    try {
      const data = await getHistory();
      setQuizzes(data);
    } catch (err) {
      setError(err.message || 'Failed to fetch quiz history');
    } finally {
      setLoading(false);
    }
  };

  const handleViewQuiz = async (quizId) => {
    setLoadingQuiz(true);
    try {
      const data = await getQuiz(quizId);
      setSelectedQuiz(data);
      setModalOpen(true);
    } catch (err) {
      setError(err.message || 'Failed to fetch quiz details');
    } finally {
      setLoadingQuiz(false);
    }
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleString();
  };

  return (
    <div className="max-w-4xl mx-auto">
      <div className="bg-white rounded-lg shadow-lg p-6">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-2xl font-bold text-gray-800">Quiz History</h2>
          <button
            onClick={fetchHistory}
            className="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors"
          >
            Refresh
          </button>
        </div>

        {error && (
          <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg mb-4">
            {error}
          </div>
        )}

        {loading ? (
          <div className="text-center py-8">
            <svg className="animate-spin h-8 w-8 text-blue-600 mx-auto" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            <p className="mt-2 text-gray-500">Loading history...</p>
          </div>
        ) : quizzes.length === 0 ? (
          <div className="text-center py-8 text-gray-500">
            No quiz history yet. Generate your first quiz!
          </div>
        ) : (
          <div className="space-y-4">
            {quizzes.map((quiz) => (
              <div
                key={quiz.id}
                className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow"
              >
                <div className="flex justify-between items-start">
                  <div className="flex-1">
                    <h3 className="text-lg font-semibold text-gray-800 mb-1">
                      {quiz.title}
                    </h3>
                    <p className="text-sm text-gray-500 mb-2">{quiz.url}</p>
                    <p className="text-xs text-gray-400">
                      {formatDate(quiz.date_generated)}
                    </p>
                  </div>
                  <button
                    onClick={() => handleViewQuiz(quiz.id)}
                    disabled={loadingQuiz}
                    className="ml-4 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-blue-400 disabled:cursor-not-allowed transition-colors"
                  >
                    {loadingQuiz ? 'Loading...' : 'View Details'}
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      <Modal isOpen={modalOpen} onClose={() => setModalOpen(false)}>
        {selectedQuiz && (
          <div>
            <div className="mb-4 pb-4 border-b">
              <h3 className="text-xl font-semibold text-gray-800">{selectedQuiz.title}</h3>
              <p className="text-sm text-gray-500 mt-1">
                Generated on {formatDate(selectedQuiz.date_generated)}
              </p>
            </div>
            <QuizDisplay quizData={selectedQuiz} />
          </div>
        )}
      </Modal>
    </div>
  );
};

export default HistoryTab;

