'use client'

import { useState } from 'react'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'

const searchSchema = z.object({
  property_address: z.object({
    street: z.string().min(1, 'Street is required'),
    city: z.string().min(1, 'City is required'),
    state: z.string().length(2, 'State must be 2 characters'),
    zip_code: z.string().min(5, 'Zip code is required'),
    county: z.string().optional(),
    parcel_number: z.string().optional(),
  }),
  search_type: z.enum(['full', 'quick', 'lien_only', 'encumbrance_only']),
  include_historical: z.boolean().default(false),
  jurisdiction: z.string().optional(),
})

type SearchFormData = z.infer<typeof searchSchema>

interface TitleSearchFormProps {
  onSubmit: (data: SearchFormData) => void
  loading: boolean
}

export default function TitleSearchForm({ onSubmit, loading }: TitleSearchFormProps) {
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<SearchFormData>({
    resolver: zodResolver(searchSchema),
    defaultValues: {
      search_type: 'full',
      include_historical: false,
    },
  })

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <h2 className="text-2xl font-semibold mb-4">New Title Search</h2>
      
      <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
        <div>
          <label className="block text-sm font-medium mb-1">Street Address</label>
          <input
            {...register('property_address.street')}
            className="w-full px-3 py-2 border rounded-md"
            placeholder="123 Main St"
          />
          {errors.property_address?.street && (
            <p className="text-red-500 text-sm mt-1">{errors.property_address.street.message}</p>
          )}
        </div>

        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium mb-1">City</label>
            <input
              {...register('property_address.city')}
              className="w-full px-3 py-2 border rounded-md"
              placeholder="Los Angeles"
            />
            {errors.property_address?.city && (
              <p className="text-red-500 text-sm mt-1">{errors.property_address.city.message}</p>
            )}
          </div>

          <div>
            <label className="block text-sm font-medium mb-1">State</label>
            <input
              {...register('property_address.state')}
              className="w-full px-3 py-2 border rounded-md"
              placeholder="CA"
              maxLength={2}
            />
            {errors.property_address?.state && (
              <p className="text-red-500 text-sm mt-1">{errors.property_address.state.message}</p>
            )}
          </div>
        </div>

        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium mb-1">Zip Code</label>
            <input
              {...register('property_address.zip_code')}
              className="w-full px-3 py-2 border rounded-md"
              placeholder="90001"
            />
            {errors.property_address?.zip_code && (
              <p className="text-red-500 text-sm mt-1">{errors.property_address.zip_code.message}</p>
            )}
          </div>

          <div>
            <label className="block text-sm font-medium mb-1">County (Optional)</label>
            <input
              {...register('property_address.county')}
              className="w-full px-3 py-2 border rounded-md"
              placeholder="Los Angeles"
            />
          </div>
        </div>

        <div>
          <label className="block text-sm font-medium mb-1">Search Type</label>
          <select
            {...register('search_type')}
            className="w-full px-3 py-2 border rounded-md"
          >
            <option value="full">Full Search</option>
            <option value="quick">Quick Search</option>
            <option value="lien_only">Lien Only</option>
            <option value="encumbrance_only">Encumbrance Only</option>
          </select>
        </div>

        <div className="flex items-center">
          <input
            type="checkbox"
            {...register('include_historical')}
            className="mr-2"
          />
          <label className="text-sm">Include Historical Records</label>
        </div>

        <button
          type="submit"
          disabled={loading}
          className="w-full bg-primary-600 text-white py-2 px-4 rounded-md hover:bg-primary-700 disabled:opacity-50"
        >
          {loading ? 'Searching...' : 'Start Title Search'}
        </button>
      </form>
    </div>
  )
}

