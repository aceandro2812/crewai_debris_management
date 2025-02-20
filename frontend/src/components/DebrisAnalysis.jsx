import React, { useState } from 'react';
import { Card, CardContent, TextField, Button, Typography, Box, CircularProgress } from '@mui/material';
import axios from 'axios';

const DebrisAnalysis = () => {
  const [debris, setDebris] = useState({ weight: '' });
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const response = await axios.post('http://localhost:8000/debris/analyze/', debris);
      setAnalysis(response.data.analysis);
    } catch (error) {
      console.error('Error analyzing debris:', error);
    }
    setLoading(false);
  };

  return (
    <Card sx={{ maxWidth: 800, margin: '20px auto' }}>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          Analyze Construction Debris
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

        {analysis && (
          <Box sx={{ mt: 4 }}>
            <Typography variant="h6" gutterBottom>
              Analysis Results
            </Typography>
            <Typography variant="body1" component="pre" sx={{ whiteSpace: 'pre-wrap' }}>
              {analysis}
            </Typography>
          </Box>
        )}
      </CardContent>
    </Card>
  );
};

export default DebrisAnalysis;