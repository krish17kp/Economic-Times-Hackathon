import React from 'react';
import { CheckCircle2, Circle, Loader2 } from 'lucide-react';

export default function ProgressSteps({ steps, currentStep }) {
    return (
        <div className="space-y-6">
            {steps.map((step, index) => {
                const isCompleted = index < currentStep;
                const isCurrent = index === currentStep;
                const isPending = index > currentStep;

                return (
                    <div key={index} className="flex items-center gap-4">
                        <div className="flex-shrink-0">
                            {isCompleted && <CheckCircle2 className="w-8 h-8 text-brand" />}
                            {isCurrent && <Loader2 className="w-8 h-8 text-blue-500 animate-spin" />}
                            {isPending && <Circle className="w-8 h-8 text-slate-300" />}
                        </div>
                        <div className={`text-lg font-medium transition-colors ${
                            isCompleted ? 'text-slate-900' :
                            isCurrent ? 'text-blue-600' : 'text-slate-400'
                        }`}>
                            {step.label}
                        </div>
                    </div>
                );
            })}
        </div>
    );
}
