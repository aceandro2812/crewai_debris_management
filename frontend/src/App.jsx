import React, { useState } from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { CssBaseline, Container } from '@mui/material';
import Navigation from './components/Navigation';
import MaterialForm from './components/MaterialForm';
import MaterialList from './components/MaterialList';
import DebrisAnalysis from './components/DebrisAnalysis';

function App() {
  const [refreshTrigger, setRefreshTrigger] = useState(0);

  const handleMaterialAdded = () => {
    setRefreshTrigger(prev => prev + 1);
  };

  return (
    <BrowserRouter>
      <CssBaseline />
      <Navigation />
      <Container sx={{ py: 4 }}>
        <Routes>
          <Route path="/" element={
            <>
              <MaterialForm onMaterialAdded={handleMaterialAdded} />
              <MaterialList refreshTrigger={refreshTrigger} />
            </>
          } />
          <Route path="/analyze" element={<DebrisAnalysis />} />
        </Routes>
      </Container>
    </BrowserRouter>
  );
}

export default App;