import React, { useState, useEffect } from 'react';
import axios from 'axios';

const Dashboard = () => {
  const [localizacoes, setLocalizacoes] = useState([]);
  const [selecionada, setSelecionada] = useState(null);
  const [clima, setClima] = useState(null);

  useEffect(() => {
    axios.get('http://localhost:5000/api/localizacoes')
      .then(res => setLocalizacoes(res.data));
  }, []);

  const handleSelecionarLocalizacao = (loc) => {
    setSelecionada(loc);
    // Buscar clima atual
  };

  return (
    <div style={{ padding: '20px' }}>
      <h1>Verificador de Clima - Obras</h1>
      <div style={{ display: 'flex', gap: '20px' }}>
        <div style={{ flex: 1 }}>
          <h2>Localizações</h2>
          {localizacoes.map(loc => (
            <button key={loc.id} onClick={() => handleSelecionarLocalizacao(loc)}>
              {loc.nome}
            </button>
          ))}
        </div>
        <div style={{ flex: 1 }}>
          {selecionada && <h2>{selecionada.nome}</h2>}
          {clima && <pre>{JSON.stringify(clima, null, 2)}</pre>}
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
