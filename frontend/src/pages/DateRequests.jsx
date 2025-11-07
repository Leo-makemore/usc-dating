import { useState, useEffect } from 'react'
import { useSearchParams } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'
import api from '../services/api'

export default function DateRequests() {
  const { user } = useAuth()
  const [searchParams] = useSearchParams()
  const [requests, setRequests] = useState([])
  const [loading, setLoading] = useState(true)
  const [showForm, setShowForm] = useState(false)
  const [formData, setFormData] = useState({
    receiver_id: '',
    message: '',
    proposed_date: '',
  })
  const [statusFilter, setStatusFilter] = useState('')

  useEffect(() => {
    fetchRequests()
    const sendTo = searchParams.get('send_to')
    if (sendTo) {
      setFormData({ ...formData, receiver_id: sendTo })
      setShowForm(true)
    }
  }, [statusFilter])

  const fetchRequests = async () => {
    try {
      setLoading(true)
      const params = statusFilter ? { status_filter: statusFilter } : {}
      const response = await api.get('/api/date-requests', { params })
      setRequests(response.data)
    } catch (error) {
      console.error('Failed to fetch date requests:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    try {
      await api.post('/api/date-requests', {
        ...formData,
        receiver_id: parseInt(formData.receiver_id),
        proposed_date: formData.proposed_date || null,
      })
      setShowForm(false)
      setFormData({ receiver_id: '', message: '', proposed_date: '' })
      fetchRequests()
    } catch (error) {
      alert(error.response?.data?.detail || 'Failed to send date request')
    }
  }

  const handleStatusUpdate = async (requestId, status) => {
    try {
      await api.put(`/api/date-requests/${requestId}`, { status })
      fetchRequests()
    } catch (error) {
      alert(error.response?.data?.detail || 'Failed to update request')
    }
  }

  if (loading) {
    return <div className="text-center py-12">Loading date requests...</div>
  }

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold text-gray-900">Date Requests</h1>
        <div className="flex space-x-4">
          <select
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value)}
            className="border border-gray-300 rounded-md px-3 py-2"
          >
            <option value="">All Status</option>
            <option value="pending">Pending</option>
            <option value="accepted">Accepted</option>
            <option value="rejected">Rejected</option>
          </select>
          <button
            onClick={() => setShowForm(!showForm)}
            className="bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded-md"
          >
            {showForm ? 'Cancel' : 'New Request'}
          </button>
        </div>
      </div>

      {showForm && (
        <div className="bg-white rounded-lg shadow-md p-6 mb-6">
          <h2 className="text-xl font-semibold mb-4">Send Date Request</h2>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700">Receiver ID</label>
              <input
                type="number"
                value={formData.receiver_id}
                onChange={(e) => setFormData({ ...formData, receiver_id: e.target.value })}
                required
                className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700">Message</label>
              <textarea
                value={formData.message}
                onChange={(e) => setFormData({ ...formData, message: e.target.value })}
                className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md"
                rows="3"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700">Proposed Date</label>
              <input
                type="datetime-local"
                value={formData.proposed_date}
                onChange={(e) => setFormData({ ...formData, proposed_date: e.target.value })}
                className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md"
              />
            </div>
            <button
              type="submit"
              className="bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded-md"
            >
              Send Request
            </button>
          </form>
        </div>
      )}

      {requests.length === 0 ? (
        <div className="text-center py-12 text-gray-500">No date requests</div>
      ) : (
        <div className="space-y-4">
          {requests.map((request) => {
            const isSender = request.sender_id === user?.id
            const otherUser = isSender ? request.receiver : request.sender

            return (
              <div key={request.id} className="bg-white rounded-lg shadow-md p-6">
                <div className="flex justify-between items-start">
                  <div>
                    <h3 className="text-lg font-semibold">
                      {isSender ? `To: ${otherUser.name}` : `From: ${otherUser.name}`}
                    </h3>
                    <p className="text-sm text-gray-500">{otherUser.school}</p>
                    {request.message && <p className="mt-2 text-gray-700">{request.message}</p>}
                    {request.proposed_date && (
                      <p className="mt-1 text-sm text-gray-600">
                        Proposed: {new Date(request.proposed_date).toLocaleString()}
                      </p>
                    )}
                    <span
                      className={`inline-block mt-2 px-2 py-1 rounded text-xs font-medium ${
                        request.status === 'accepted'
                          ? 'bg-green-100 text-green-800'
                          : request.status === 'rejected'
                          ? 'bg-red-100 text-red-800'
                          : 'bg-yellow-100 text-yellow-800'
                      }`}
                    >
                      {request.status}
                    </span>
                  </div>
                  {!isSender && request.status === 'pending' && (
                    <div className="flex space-x-2">
                      <button
                        onClick={() => handleStatusUpdate(request.id, 'accepted')}
                        className="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-md text-sm"
                      >
                        Accept
                      </button>
                      <button
                        onClick={() => handleStatusUpdate(request.id, 'rejected')}
                        className="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-md text-sm"
                      >
                        Reject
                      </button>
                    </div>
                  )}
                </div>
              </div>
            )
          })}
        </div>
      )}
    </div>
  )
}

