/**
 * Calculates a confidence level based on a model prediction score.
 * 
 * @param {number} modelPredictionScore - A number between 0 and 1 representing the model's prediction score
 * @returns {string} The confidence level: "High", "Medium", or "Low"
 * @throws {Error} If modelPredictionScore is not a number or is outside the range [0, 1]
 */
export const calculateConfidenceScore = (modelPredictionScore) => {
    // Validate input
    if (typeof modelPredictionScore !== 'number' || modelPredictionScore < 0 || modelPredictionScore > 1) {
        throw new Error('modelPredictionScore must be a number between 0 and 1');
    }

    if (modelPredictionScore > 0.8) {
        return "High";
    } else if (modelPredictionScore > 0.6) {
        return "Medium";
    } else {
        return "Low";
    }
}; 