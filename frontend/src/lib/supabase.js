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
 * Upload a file to Supabase Storage
 * @param {File} file - File to upload
 * @param {string} albumSlug - Album slug (me, travel, sports, etc.)
 * @returns {Promise<{url: string, path: string}>}
 */
export async function uploadFile(file, albumSlug) {
  if (!file) throw new Error('No file provided')
  if (!albumSlug) throw new Error('Album slug required')

  // Generate unique filename
  const fileExt = file.name.split('.').pop()
  const timestamp = Date.now()
  const fileName = `${timestamp}-${Math.random().toString(36).substring(2, 9)}.${fileExt}`
  const filePath = `${albumSlug}/${fileName}`

  // Upload to Supabase Storage
  const { data, error } = await supabase.storage
    .from('photos')
    .upload(filePath, file, {
      cacheControl: '3600',
      upsert: false
    })

  if (error) {
    throw new Error(`Upload failed: ${error.message}`)
  }

  // Get public URL
  const { data: { publicUrl } } = supabase.storage
    .from('photos')
    .getPublicUrl(data.path)

  return {
    url: publicUrl,
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
