class ClimaManager {
    constructor() {
        this.apiUrl = 'http://localhost:5000/api';
        this.obras = [];
        this.marcadores = {};
    }

    // Buscar clima de uma única localização
    async buscarClima(lat, lon) {
        try {
            const response = await fetch(`${this.apiUrl}/clima/${lat}/${lon}`);
            if (!response.ok) throw new Error('Erro ao buscar clima');
            return await response.json();
        } catch (error) {
            console.error('Erro:', error);
            return null;
        }
    }

    // Buscar clima de múltiplas obras
    async buscarClimaObras(obras) {
        try {
            const response = await fetch(`${this.apiUrl}/obras/clima`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ obras })
            });
            if (!response.ok) throw new Error('Erro ao buscar clima das obras');
            return await response.json();
        } catch (error) {
            console.error('Erro:', error);
            return null;
        }
    }

    // Atualizar card de obra com clima
    async atualizarCardObra(obraId, lat, lon) {
        const clima = await this.buscarClima(lat, lon);
        if (!clima) return;

        const card = document.querySelector(`[data-obra-id="${obraId}"]`);
        if (!card) return;

        const climaDiv = card.querySelector('.clima-info') || document.createElement('div');
        climaDiv.className = 'clima-info';
        climaDiv.innerHTML = `
            <div class="clima-item">
                <strong>🌡️ Temperatura:</strong> ${clima.temperatura}°C
            </div>
            <div class="clima-item">
                <strong>💧 Chuva:</strong> ${clima.chuva} mm
            </div>
            <div class="clima-item">
                <strong>☁️ Nuvens:</strong> ${clima.nuvens}%
            </div>
            <div class="clima-item">
                <strong>💨 Vento:</strong> ${clima.velocidade_vento} m/s
            </div>
            <div class="clima-item">
                <strong>💧 Umidade:</strong> ${clima.humidade}%
            </div>
        `;
        
        if (!card.querySelector('.clima-info')) {
            card.appendChild(climaDiv);
        }
    }

    // Adicionar overlay de chuva e nuvens no mapa
    adicionarOverlayMapa(map, obras) {
        obras.forEach(obra => {
            const marker = this.marcadores[obra.id];
            if (marker) {
                const popupContent = `
                    <div class="popup-clima">
                        <strong>${obra.nome}</strong><br>
                        🌧️ Chuva: ${obra.chuva} mm<br>
                        ☁️ Nuvens: ${obra.nuvens}%<br>
                        🌡️ Temp: ${obra.temperatura}°C
                    </div>
                `;
                marker.setPopupContent(popupContent);
                
                // Mudar cor do marcador baseado em chuva
                if (obra.chuva > 10) {
                    marker.setIcon(L.icon({
                        iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-blue.png',
                        shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
                        iconSize: [25, 41],
                        iconAnchor: [12, 41],
                        popupAnchor: [1, -34],
                        shadowSize: [41, 41]
                    }));
                }
            }
        });
    }

    // Atualizar todos os dados de clima
    async atualizar(obras, map) {
        const result = await this.buscarClimaObras(obras);
        if (result && result.obras) {
            this.adicionarOverlayMapa(map, result.obras);
            
            // Atualizar cards
            result.obras.forEach(obra => {
                const card = document.querySelector(`[data-obra-id="${obra.id}"]`);
                if (card) {
                    this.atualizarCardObra(obra.id, obra.lat, obra.lon);
                }
            });
        }
    }

    // Registrar marcador para referência posterior
    registrarMarcador(obraId, marker) {
        this.marcadores[obraId] = marker;
    }
}

// Instância global
const climaManager = new ClimaManager();
