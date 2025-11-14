import React from "react";
import { X } from "lucide-react";
import { Button } from "@/components/ui/button";

const FilterPanel = ({ filters, setFilters, onApply }) => {
  const dietaryOptions = [
    "vegetarian",
    "vegan",
    "gluten-free",
    "dairy-free",
    "low-carb",
    "high-protein"
  ];

  const toggleDietaryTag = (tag) => {
    if (filters.dietaryTags.includes(tag)) {
      setFilters({
        ...filters,
        dietaryTags: filters.dietaryTags.filter(t => t !== tag)
      });
    } else {
      setFilters({
        ...filters,
        dietaryTags: [...filters.dietaryTags, tag]
      });
    }
  };

  const clearFilters = () => {
    setFilters({
      difficulty: "",
      maxCookingTime: "",
      dietaryTags: []
    });
  };

  return (
    <div className="card" data-testid="filter-panel">
      <div className="flex items-center justify-between mb-6">
        <h3 className="text-xl font-bold">Filters</h3>
        <button 
          onClick={clearFilters}
          className="text-sm text-orange-600 hover:text-orange-700 font-medium"
          data-testid="clear-filters-btn"
        >
          Clear All
        </button>
      </div>

      <div className="grid md:grid-cols-3 gap-6">
        {/* Difficulty */}
        <div>
          <label className="block text-sm font-medium mb-2">Difficulty</label>
          <select
            value={filters.difficulty}
            onChange={(e) => setFilters({...filters, difficulty: e.target.value})}
            className="w-full px-4 py-2 border-2 border-gray-200 rounded-xl focus:border-orange-400 focus:outline-none"
            data-testid="difficulty-filter"
          >
            <option value="">Any</option>
            <option value="easy">Easy</option>
            <option value="medium">Medium</option>
            <option value="hard">Hard</option>
          </select>
        </div>

        {/* Cooking Time */}
        <div>
          <label className="block text-sm font-medium mb-2">Max Cooking Time (mins)</label>
          <input
            type="number"
            value={filters.maxCookingTime}
            onChange={(e) => setFilters({...filters, maxCookingTime: e.target.value})}
            placeholder="e.g., 30"
            className="w-full px-4 py-2 border-2 border-gray-200 rounded-xl focus:border-orange-400 focus:outline-none"
            data-testid="cooking-time-filter"
          />
        </div>

        {/* Dietary Preferences */}
        <div className="md:col-span-1">
          <label className="block text-sm font-medium mb-2">Dietary Preferences</label>
          <div className="flex flex-wrap gap-2">
            {dietaryOptions.map((option) => (
              <button
                key={option}
                onClick={() => toggleDietaryTag(option)}
                className={`px-3 py-1 rounded-full text-sm font-medium transition-all ${
                  filters.dietaryTags.includes(option)
                    ? 'bg-orange-500 text-white'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
                data-testid={`dietary-tag-${option}`}
              >
                {option}
              </button>
            ))}
          </div>
        </div>
      </div>

      <div className="mt-6 flex justify-end">
        <button 
          onClick={onApply}
          className="btn btn-primary"
          data-testid="apply-filters-btn"
        >
          Apply Filters
        </button>
      </div>
    </div>
  );
};

export default FilterPanel;