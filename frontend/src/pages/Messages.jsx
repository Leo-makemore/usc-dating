import { useState, useEffect, useRef } from 'react'
import { useSearchParams } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'
import api from '../services/api'

export default function Messages() {
  const { user } = useAuth()
  const [searchParams] = useSearchParams()
  const [conversations, setConversations] = useState([])
  const [messages, setMessages] = useState([])
  const [selectedUser, setSelectedUser] = useState(null)
  const [newMessage, setNewMessage] = useState('')
  const [loading, setLoading] = useState(true)
  const messagesEndRef = useRef(null)

  useEffect(() => {
    fetchConversations()
    const userId = searchParams.get('user')
    if (userId) {
      setSelectedUser(parseInt(userId))
    }
  }, [])

  useEffect(() => {
    if (selectedUser) {
      fetchMessages(selectedUser)
    }
  }, [selectedUser])

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  const fetchConversations = async () => {
    try {
      const response = await api.get('/api/messages')
      // Group messages by other user
      const userMap = new Map()
      response.data.forEach((msg) => {
        const otherUser = msg.sender_id === user?.id ? msg.receiver : msg.sender
        if (!userMap.has(otherUser.id)) {
          userMap.set(otherUser.id, {
            user: otherUser,
            lastMessage: msg,
            unread: msg.receiver_id === user?.id && !msg.is_read,
          })
        } else {
          const existing = userMap.get(otherUser.id)
          if (new Date(msg.created_at) > new Date(existing.lastMessage.created_at)) {
            existing.lastMessage = msg
          }
          if (msg.receiver_id === user?.id && !msg.is_read) {
            existing.unread = true
          }
        }
      })
      setConversations(Array.from(userMap.values()))
    } catch (error) {
      console.error('Failed to fetch conversations:', error)
    } finally {
      setLoading(false)
    }
  }

  const fetchMessages = async (otherUserId) => {
    try {
      const response = await api.get('/api/messages', {
        params: { other_user_id: otherUserId },
      })
      setMessages(response.data)
      // Mark messages as read
      response.data.forEach((msg) => {
        if (msg.receiver_id === user?.id && !msg.is_read) {
          api.put(`/api/messages/${msg.id}/read`)
        }
      })
    } catch (error) {
      console.error('Failed to fetch messages:', error)
    }
  }

  const sendMessage = async (e) => {
    e.preventDefault()
    if (!newMessage.trim() || !selectedUser) return

    try {
      await api.post('/api/messages', {
        receiver_id: selectedUser,
        content: newMessage,
      })
      setNewMessage('')
      fetchMessages(selectedUser)
      fetchConversations()
    } catch (error) {
      alert(error.response?.data?.detail || 'Failed to send message')
    }
  }

  if (loading) {
    return <div className="text-center py-12">Loading messages...</div>
  }

  const selectedConversation = conversations.find((c) => c.user.id === selectedUser)

  return (
    <div className="flex h-[calc(100vh-200px)]">
      {/* Conversations List */}
      <div className="w-1/3 border-r border-gray-200 overflow-y-auto">
        <div className="p-4 border-b border-gray-200">
          <h2 className="text-xl font-semibold">Conversations</h2>
        </div>
        {conversations.length === 0 ? (
          <div className="p-4 text-center text-gray-500">No conversations</div>
        ) : (
          <div>
            {conversations.map((conv) => (
              <div
                key={conv.user.id}
                onClick={() => setSelectedUser(conv.user.id)}
                className={`p-4 border-b border-gray-200 cursor-pointer hover:bg-gray-50 ${
                  selectedUser === conv.user.id ? 'bg-indigo-50' : ''
                }`}
              >
                <div className="flex items-center space-x-3">
                  {conv.user.avatar_url ? (
                    <img
                      src={conv.user.avatar_url}
                      alt={conv.user.name}
                      className="w-12 h-12 rounded-full object-cover"
                    />
                  ) : (
                    <div className="w-12 h-12 rounded-full bg-indigo-100 flex items-center justify-center">
                      <span className="text-indigo-600 font-semibold">
                        {conv.user.name.charAt(0).toUpperCase()}
                      </span>
                    </div>
                  )}
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center justify-between">
                      <p className="text-sm font-medium text-gray-900">{conv.user.name}</p>
                      {conv.unread && (
                        <span className="w-2 h-2 bg-indigo-600 rounded-full"></span>
                      )}
                    </div>
                    <p className="text-sm text-gray-500 truncate">
                      {conv.lastMessage.content}
                    </p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Messages Area */}
      <div className="flex-1 flex flex-col">
        {selectedUser ? (
          <>
            <div className="p-4 border-b border-gray-200">
              <h3 className="text-lg font-semibold">
                {selectedConversation?.user.name || 'User'}
              </h3>
            </div>
            <div className="flex-1 overflow-y-auto p-4 space-y-4">
              {messages.map((msg) => {
                const isOwn = msg.sender_id === user?.id
                return (
                  <div
                    key={msg.id}
                    className={`flex ${isOwn ? 'justify-end' : 'justify-start'}`}
                  >
                    <div
                      className={`max-w-xs lg:max-w-md px-4 py-2 rounded-lg ${
                        isOwn
                          ? 'bg-indigo-600 text-white'
                          : 'bg-gray-200 text-gray-900'
                      }`}
                    >
                      <p>{msg.content}</p>
                      <p
                        className={`text-xs mt-1 ${
                          isOwn ? 'text-indigo-200' : 'text-gray-500'
                        }`}
                      >
                        {new Date(msg.created_at).toLocaleTimeString()}
                      </p>
                    </div>
                  </div>
                )
              })}
              <div ref={messagesEndRef} />
            </div>
            <form onSubmit={sendMessage} className="p-4 border-t border-gray-200">
              <div className="flex space-x-2">
                <input
                  type="text"
                  value={newMessage}
                  onChange={(e) => setNewMessage(e.target.value)}
                  placeholder="Type a message..."
                  className="flex-1 px-4 py-2 border border-gray-300 rounded-md focus:ring-indigo-500 focus:border-indigo-500"
                />
                <button
                  type="submit"
                  className="bg-indigo-600 hover:bg-indigo-700 text-white px-6 py-2 rounded-md"
                >
                  Send
                </button>
              </div>
            </form>
          </>
        ) : (
          <div className="flex-1 flex items-center justify-center text-gray-500">
            Select a conversation to start messaging
          </div>
        )}
      </div>
    </div>
  )
}

