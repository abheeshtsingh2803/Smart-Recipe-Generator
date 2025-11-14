import React from "react";
import { Activity } from "lucide-react";

const NutritionInfo = ({ nutrition }) => {
  if (!nutrition) return null;

  const nutritionItems = [
    { label: "Calories", value: nutrition.calories, unit: "kcal", color: "bg-orange-500" },
    { label: "Protein", value: nutrition.protein, unit: "g", color: "bg-red-500" },
    { label: "Carbs", value: nutrition.carbs, unit: "g", color: "bg-yellow-500" },
    { label: "Fat", value: nutrition.fat, unit: "g", color: "bg-purple-500" },
    { label: "Fiber", value: nutrition.fiber, unit: "g", color: "bg-green-500" }
  ];

  return (
    <div className="card sticky top-24" data-testid="nutrition-info">
      <div className="flex items-center mb-6">
        <Activity className="w-6 h-6 text-orange-500 mr-2" />
        <h3 className="text-2xl font-bold">Nutrition Facts</h3>
      </div>
      
      <p className="text-sm text-gray-600 mb-6">Per Serving</p>

      <div className="space-y-4">
        {nutritionItems.map((item, index) => (
          <div key={index} className="space-y-2">
            <div className="flex justify-between items-center">
              <span className="font-medium text-gray-700">{item.label}</span>
              <span className="font-bold text-gray-900">
                {item.value} {item.unit}
              </span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-2 overflow-hidden">
              <div 
                className={`h-full ${item.color} rounded-full transition-all duration-500`}
                style={{ width: `${Math.min((item.value / (item.label === 'Calories' ? 600 : 50)) * 100, 100)}%` }}
              ></div>
            </div>
          </div>
        ))}
      </div>

      <div className="mt-6 pt-6 border-t text-xs text-gray-500">
        * Nutritional values are estimates and may vary based on portion sizes and ingredients used.
      </div>
    </div>
  );
};

export default NutritionInfo;