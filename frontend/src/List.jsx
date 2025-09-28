import { useState, useEffect } from 'react'
import axios from 'axios'

const API_URL = 'http://localhost:8000'

export default function ist(){

    // Todo 추가 // pick
    const addTodo = async (e) => {
    e.preventDefault()
    if (!newTodo.trim()) return

    try {
        const response = await axios.post(`${API_URL}/todos`, {
        title: newTodo.trim(),
        description: newDescription.trim() || undefined
        })
        setTodos([...todos, response.data])
        setNewTodo('')
        setNewDescription('')
        setError('')
    } catch (err) {
        setError('할 일 추가에 실패했습니다.')
        console.error(err)
    }
    }

    return (
        <>
            // Todo 추가 폼
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
          </div>
        </>
    );

};
