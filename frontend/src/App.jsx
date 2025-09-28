import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom';
import List from './List';
import axios from 'axios'

const API_URL = 'http://localhost:8000'

export default function App() {
  const [todos, setTodos] = useState([])
  const [newTodo, setNewTodo] = useState('')
  const [newDescription, setNewDescription] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  // 모달 상태
  const [isModalOpen, setIsModalOpen] = useState(false)
  const [selectedTodo, setSelectedTodo] = useState(null)

  // Todo 목록 조회 // rendering
  const fetchTodos = async () => {
    try {
      setLoading(true)
      const response = await axios.get(`${API_URL}/todos`)
      setTodos(response.data)
    } catch (err) {
      setError('할 일을 불러오는데 실패했습니다.')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  // Todo 추가 // pick
  // const addTodo = async (e) => {
  //   e.preventDefault()
  //   if (!newTodo.trim()) return

  //   try {
  //     const response = await axios.post(`${API_URL}/todos`, {
  //       title: newTodo.trim(),
  //       description: newDescription.trim() || undefined
  //     })
  //     setTodos([...todos, response.data])
  //     setNewTodo('')
  //     setNewDescription('')
  //     setError('')
  //   } catch (err) {
  //     setError('할 일 추가에 실패했습니다.')
  //     console.error(err)
  //   }
  // }

  // 커스텀 모달 열기
  const openDeleteModal = (todo) => {
    setSelectedTodo(todo)
    setIsModalOpen(true)
  }

  // 모달에서 삭제 확정
  const confirmDelete = async () => {
    if (!selectedTodo) return
    try {
      await axios.delete(`${API_URL}/todos/${selectedTodo.id}`)
      setTodos(todos.filter(todo => todo.id !== selectedTodo.id))
      setSelectedTodo(null)
      setIsModalOpen(false)
    } catch (err) {
      setError('할 일 삭제에 실패했습니다.')
      console.error(err)
    }
  }

  // Todo 완료 상태 토글
  const toggleTodo = async (id) => {
    try {
      const response = await axios.patch(`${API_URL}/todos/${id}/toggle`)
      setTodos(todos.map(todo => todo.id === id ? response.data : todo))
    } catch (err) {
      setError('상태 변경에 실패했습니다.')
      console.error(err)
    }
  }

  // 랜더링용 action, 즉 return 하기 전에 한번 <todo>데이터 불러오기 전용
  useEffect(() => {
    fetchTodos()
  },[]) // 빈 배열이면 한번만 수행하겠다는 거, 안에 값을 넣으면, 해당 값이 변할 때 마다 새로 불러옴.

  return (
    <>
      <div className="min-h-screen bg-gray-50 py-8 flex flex-col items-center justify-center">
        <div className="w-full max-w-2xl px-4 py-8 bg-white rounded-lg shadow-md">
          {/* 헤더 */}
          <header className="text-center mb-8">
            <h1 className="text-4xl font-bold text-gray-900 mb-2">📝 Todo App</h1>
          </header>

          {/* 에러 메시지 */}
          {error && (
            <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-6">
              <div className="flex justify-between items-center">
                <span>{error}</span>
                <button 
                  onClick={() => setError('')}
                  className="text-red-500 hover:text-red-700 font-bold"
                >
                  ×
                </button>
              </div>
            </div>
          )}

          {/* Todo 추가 폼
          <div className="bg-white rounded-lg shadow-md p-6 mb-8">
            <form onSubmit={addTodo}>
              <div className="mb-4">
                <input
                  type="text"
                  placeholder="할 일을 입력하세요..."
                  value={newTodo}
                  onChange={(e) => setNewTodo(e.target.value)}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>
              <div className="mb-4">
                <textarea
                  placeholder="설명 (선택사항)"
                  value={newDescription}
                  onChange={(e) => setNewDescription(e.target.value)}
                  rows={2}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
                />
              </div>
              <button
                type="submit"
                disabled={!newTodo.trim()}
                className="w-full bg-blue-500 hover:bg-blue-600 disabled:bg-gray-300 disabled:cursor-not-allowed text-white font-semibold py-3 px-4 rounded-lg transition duration-200"
              >
                ➕ 할 일 추가
              </button>
            </form>
          </div> */}

          {/* 로딩 */}
          {loading && (
            <div className="text-center py-8">
              <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
              <p className="mt-2 text-gray-600">로딩 중...</p>
            </div>
          )}

          {/* 라우팅 버튼 */}
          <Link to="List">
            <div className="mb-4 text-right">
              <button
                onClick={() => window.location.href = '/list'}
                className="bg-green-500 hover:bg-green-600 text-white font-semibold py-2 px-4 rounded-lg transition duration-200"
              >
                ➕ 새로운 할 일 추가하기
              </button>
            </div>
          </Link>  

          {/* Todo 목록 */}
          <div className="bg-white rounded-lg shadow-md">
            <div className="px-6 py-4 border-b border-gray-200">
              <h2 className="text-xl font-semibold text-gray-900">
                할 일 목록 ({todos.length}개)
              </h2>
            </div>

            {todos.length === 0 ? (
              <div className="px-6 py-12 text-center">
                <div className="text-6xl mb-4">📝</div>
                <p className="text-gray-500 text-lg">할 일이 없습니다</p>
                <p className="text-gray-400 mt-1">새로운 할 일을 추가해보세요!</p>
              </div>
            ) : (
              <div className="divide-y divide-gray-200">
                {todos.map((todo) => (
                  <div key={todo.id} className="px-6 py-4 hover:bg-gray-50 transition duration-150">
                    <div className="flex items-start space-x-3">
                      {/* 체크박스 */}
                      <input
                        type="checkbox"
                        checked={todo.completed}
                        onChange={() => toggleTodo(todo.id)}
                        className="mt-1 h-5 w-5 text-blue-600 rounded focus:ring-blue-500"
                      />
                      
                      {/* Todo 내용 */}
                      <div className="flex-1 min-w-0">
                        <h3 className={`text-lg font-medium ${
                          todo.completed 
                            ? 'line-through text-gray-500' 
                            : 'text-gray-900'
                        }`}>
                          {todo.title}
                        </h3>
                        
                        {todo.description && (
                          <p className={`mt-1 text-sm ${
                            todo.completed ? 'text-gray-400' : 'text-gray-600'
                          }`}>
                            {todo.description}
                          </p>
                        )}
                        
                        <div className="mt-2 flex items-center space-x-4 text-sm text-gray-500">
                          <span>
                            생성일: {new Date(todo.created_at).toLocaleDateString('ko-KR')}
                          </span>
                          {todo.completed && (
                            <span className="bg-green-100 text-green-800 px-2 py-1 rounded-full text-xs font-medium">
                              완료
                            </span>
                          )}
                        </div>
                      </div>
                      
                      {/* ✅ 커스텀 모달 열기 버튼 */}
                      <button
                        onClick={() => openDeleteModal(todo)}
                        className="text-red-500 hover:text-red-700 hover:bg-red-50 p-2 rounded-lg transition duration-200"
                        title="삭제"
                      >
                        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path>
                        </svg>
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* 커스텀 모달 */}
          {isModalOpen && (
            <div className="fixed inset-0 flex items-center justify-center bg-black/40 z-50">
              <div className="bg-white rounded-lg shadow-lg p-6 w-full max-w-md">
                <h2 className="text-xl font-semibold text-gray-900 mb-4">
                  정말 삭제하시겠습니까?
                </h2>
                <p className="text-gray-600 mb-6">
                  "{selectedTodo?.title}" 할 일이 삭제됩니다. 이 작업은 되돌릴 수 없습니다.
                </p>
                <div className="flex justify-end space-x-3">
                  <button
                    onClick={() => setIsModalOpen(false)}
                    className="px-4 py-2 rounded-lg bg-gray-200 hover:bg-gray-300 transition"
                  >
                    취소
                  </button>
                  <button
                    onClick={confirmDelete}
                    className="px-4 py-2 rounded-lg bg-red-500 text-white hover:bg-red-600 transition"
                  >
                    삭제
                  </button>
                </div>
              </div>
            </div>
          )}

          {/* 푸터 */}
          <footer className="mt-12 text-center text-gray-500 text-sm">
            <p>React 19 + JavaScript + Tailwind CSS + Vite 7</p>
          </footer>
        </div>
      </div>
    </>
  )
}

