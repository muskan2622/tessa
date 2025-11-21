'use client'

import { useState } from 'react'
import TitleSearchForm from '@/components/TitleSearchForm'
import SearchResults from '@/components/SearchResults'
import { TitleSearchResult } from '@/types/api'

export default function Home() {
  const [searchResult, setSearchResult] = useState<TitleSearchResult | null>(null)
  const [loading, setLoading] = useState(false)

  const handleSearch = async (searchData: any) => {
    setLoading(true)
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/title-search/search`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`,
        },
        body: JSON.stringify(searchData),
      })
      
      if (response.ok) {
        const result = await response.json()
        setSearchResult(result)
      } else {
        console.error('Search failed')
      }
    } catch (error) {
      console.error('Error:', error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <main className="min-h-screen p-8">
      <div className="max-w-7xl mx-auto">
        <h1 className="text-4xl font-bold mb-8">Real Estate TC Agent</h1>
        
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          <div>
            <TitleSearchForm onSubmit={handleSearch} loading={loading} />
          </div>
          
          <div>
            {searchResult && <SearchResults result={searchResult} />}
          </div>
        </div>
      </div>
    </main>
  )
}

