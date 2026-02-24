/**
 * Supabase client for frontend
 * Used for direct uploads to Supabase Storage
 */
import { createClient } from '@supabase/supabase-js'

const supabaseUrl = import.meta.env.VITE_SUPABASE_URL
const supabaseAnonKey = import.meta.env.VITE_SUPABASE_ANON_KEY

if (!supabaseUrl || !supabaseAnonKey) {
  console.warn('Supabase credentials not found. File uploads will not work.')
}

export const supabase = createClient(supabaseUrl || '', supabaseAnonKey || '')

/**
 * Upload a file to Supabase Storage via backend API
 * Uses backend service role to bypass RLS policies
 * @param {File} file - File to upload
 * @param {string} albumSlug - Album slug (me, travel, sports, etc.)
 * @param {string} adminToken - Admin authentication token
 * @returns {Promise<{url: string, path: string}>}
 */
export async function uploadFile(file, albumSlug, adminToken) {
  if (!file) throw new Error('No file provided')
  if (!albumSlug) throw new Error('Album slug required')
  if (!adminToken) throw new Error('Admin authentication required')

  const API_BASE_URL = import.meta.env.VITE_API_URL

  // Create form data
  const formData = new FormData()
  formData.append('file', file)
  formData.append('album', albumSlug)

  // Upload via backend API (which has service role access)
  const response = await fetch(`${API_BASE_URL}/admin/upload`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${adminToken}`
    },
    body: formData
  })

  if (!response.ok) {
    const error = await response.json().catch(() => ({ error: 'Upload failed' }))
    throw new Error(error.error || 'Upload failed')
  }

  const data = await response.json()
  return {
    url: data.url,
    path: data.path
  }
}

/**
 * Delete a file from Supabase Storage
 * @param {string} filePath - Path to file in storage (e.g., "me/1234.jpg")
 * @returns {Promise<void>}
 */
export async function deleteFile(filePath) {
  if (!filePath) throw new Error('File path required')

  const { error } = await supabase.storage
    .from('photos')
    .remove([filePath])

  if (error) {
    throw new Error(`Delete failed: ${error.message}`)
  }
}
