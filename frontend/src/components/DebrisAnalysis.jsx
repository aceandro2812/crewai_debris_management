import React, { useState } from 'react';
import { Card, CardContent, TextField, Button, Typography, Box, CircularProgress } from '@mui/material';
import axios from 'axios';

const DebrisAnalysis = () => {
  const [debris, setDebris] = useState({ weight: '' });
  const [analysisResults, setAnalysisResults] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const response = await axios.post('http://localhost:8000/debris/analyze/', debris);
      setAnalysisResults(response.data.analysis);
    } catch (error) {
      console.error('Error analyzing debris:', error);
    }
    setLoading(false);
  };

  const renderAnalysisSection = (title, data) => {
    if (!data) return null;
    return (
      <Box sx={{ mt: 3 }}>
        <Typography variant="h6" gutterBottom>
          {title}
        </Typography>
        <Typography variant="body1" component="pre" sx={{ whiteSpace: 'pre-wrap', backgroundColor: '#f5f5f5', p: 2, borderRadius: 1 }}>
          {typeof data === 'object' ? JSON.stringify(data, null, 2) : data}
        </Typography>
      </Box>
    );
  };

  return (
    <Card sx={{ maxWidth: 800, margin: '20px auto' }}>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          Debris Analysis
        </Typography>
        <Box component="form" onSubmit={handleSubmit}>
          <TextField
            fullWidth
            label="Debris Weight (kg)"
            type="number"
            value={debris.weight}
            onChange={(e) => setDebris({ weight: e.target.value })}
            margin="normal"
            required
          />
          <Button
            type="submit"
            variant="contained"
            color="primary"
            sx={{ mt: 2 }}
            disabled={loading}
          >
            Analyze Debris
          </Button>
        </Box>

        {loading && (
          <Box sx={{ display: 'flex', justifyContent: 'center', mt: 4 }}>
            <CircularProgress />
          </Box>
        )}

        {analysisResults && (
          <Box sx={{ mt: 4 }}>
            {renderAnalysisSection('Composition Analysis', analysisResults.analysis)}
            {renderAnalysisSection('Disposal Strategies', analysisResults.disposal)}
            {renderAnalysisSection('Environmental Impact', analysisResults.environmental_impact)}
          </Box>
        )}
      </CardContent>
    </Card>
  );
};

export default DebrisAnalysis;