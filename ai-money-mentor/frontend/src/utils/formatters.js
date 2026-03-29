export const formatCurrency = (value) => {
    if (value === undefined || value === null) return '₹0';
    if (value >= 100000) {
        return `₹${(value / 100000).toFixed(2)}L`;
    }
    return new Intl.NumberFormat('en-IN', {
        style: 'currency',
        currency: 'INR',
        maximumFractionDigits: 0
    }).format(value);
};

export const formatPercentage = (value) => {
    if (value === undefined || value === null) return '0%';
    return `${value > 0 ? '+' : ''}${value.toFixed(1)}%`;
};
