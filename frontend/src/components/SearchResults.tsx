'use client'

import { TitleSearchResult } from '@/types/api'

interface SearchResultsProps {
  result: TitleSearchResult
}

export default function SearchResults({ result }: SearchResultsProps) {
  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <h2 className="text-2xl font-semibold mb-4">Search Results</h2>
      
      <div className="space-y-4">
        <div>
          <h3 className="font-medium">Status</h3>
          <p className="text-sm text-gray-600">{result.status}</p>
        </div>

        {result.risk_score !== null && (
          <div>
            <h3 className="font-medium">Risk Score</h3>
            <p className="text-sm text-gray-600">{result.risk_score}/100</p>
          </div>
        )}

        {result.deeds.length > 0 && (
          <div>
            <h3 className="font-medium mb-2">Deeds ({result.deeds.length})</h3>
            <div className="space-y-2">
              {result.deeds.map((deed, idx) => (
                <div key={idx} className="border-l-4 border-blue-500 pl-3 py-1">
                  <p className="text-sm font-medium">{deed.deed_type}</p>
                  <p className="text-xs text-gray-600">
                    {deed.grantor} → {deed.grantee}
                  </p>
                  <p className="text-xs text-gray-500">
                    Recorded: {new Date(deed.recording_date).toLocaleDateString()}
                  </p>
                </div>
              ))}
            </div>
          </div>
        )}

        {result.liens.length > 0 && (
          <div>
            <h3 className="font-medium mb-2">Liens ({result.liens.length})</h3>
            <div className="space-y-2">
              {result.liens.map((lien, idx) => (
                <div key={idx} className="border-l-4 border-red-500 pl-3 py-1">
                  <p className="text-sm font-medium">{lien.lien_type}</p>
                  <p className="text-xs text-gray-600">Creditor: {lien.creditor}</p>
                  {lien.amount && (
                    <p className="text-xs text-gray-600">Amount: ${lien.amount.toLocaleString()}</p>
                  )}
                  <p className="text-xs text-gray-500">
                    Recorded: {new Date(lien.recording_date).toLocaleDateString()}
                  </p>
                </div>
              ))}
            </div>
          </div>
        )}

        {result.encumbrances.length > 0 && (
          <div>
            <h3 className="font-medium mb-2">Encumbrances ({result.encumbrances.length})</h3>
            <div className="space-y-2">
              {result.encumbrances.map((encumbrance, idx) => (
                <div key={idx} className="border-l-4 border-yellow-500 pl-3 py-1">
                  <p className="text-sm font-medium">{encumbrance.encumbrance_type}</p>
                  <p className="text-xs text-gray-600">{encumbrance.description}</p>
                  <p className="text-xs text-gray-500">
                    Recorded: {new Date(encumbrance.recording_date).toLocaleDateString()}
                  </p>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

