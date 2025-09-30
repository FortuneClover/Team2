import { useState, useEffect } from 'react'
import axios from 'axios'
import { Link } from 'react-router-dom';
import App from './App'

const API_URL = 'http://localhost:8000'

export default function List(){
  const [newPost, setNewPost] = useState('')
  const [newDescription, setNewDescription] = useState('')
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('') // ✅ 추가
    // Post 추가 // pick
    const addPost = async (e) => {
    e.preventDefault()
    if (!newPost.trim()) return

    try {
        const response = await axios.post(`${API_URL}/posts`, {
        title: newPost.trim(),
        content: newDescription.trim() || undefined
        })
        setNewPost('')
        setNewDescription('')
        setError('')
        setSuccess('✅ 할 일이 성공적으로 추가되었습니다!')
    } catch (err) {
        setError('할 일 추가에 실패했습니다.')
        console.error(err)
    }
    }

    return (
      <>
        {/* // Post 추가 폼 */}
        <div className="bg-white rounded-lg shadow-md p-6 mb-8">
          <form onSubmit={addPost}>
            <div className="mb-4">
              <input
                type="text"
                placeholder="할 일을 입력하세요..."
                value={newPost}
                onChange={(e) => setNewPost(e.target.value)}
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
              disabled={!newPost.trim()}
              className="w-full bg-blue-500 hover:bg-blue-600 disabled:bg-gray-300 disabled:cursor-not-allowed text-white font-semibold py-3 px-4 rounded-lg transition duration-200"
            >
              ➕ 할 일 추가
            </button>

            {/* ✅ 성공 메시지 */}
            {success && (
              <div className="bg-green-100 text-green-700 p-3 rounded mb-4">
                {success}
              </div>
            )}

            {/* 에러 메시지 */}
            {error && (
              <div className="bg-red-100 text-red-700 p-3 rounded mb-4">
                {error}
              </div>
            )}

            {/* 라우팅 버튼 */}
            <Link to="/">
            <div className="mb-4 text-right my-10">
            <button
              onClick={() => window.location.href = '/'}
              className="bg-green-500 hover:bg-green-600 text-white font-semibold py-2 px-4 rounded-lg transition duration-200"
            >
              ➕ 게시판으로 돌아가기
            </button>
            </div>
          </Link>
          </form>
        </div>
      </>
    );
};
