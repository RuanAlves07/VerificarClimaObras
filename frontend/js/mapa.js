class MapaClima {
    constructor() {
        this.map = null;
        this.marcadores = {};
        this.visualizacaoAtiva = 'temperatura';
        this.obras = [];
        this.gradientTemp = this.criarGradienteTemperatura();
        this.inicializar();
    }

    inicializar() {
        // Inicializar mapa
        this.map = L.map('mapa').setView([-5.8035, -35.2087], 12);

        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '© OpenStreetMap contributors',
            maxZoom: 19
        }).addTo(this.map);

        // Configurar controles de visualização
        document.querySelectorAll('input[name="visualizacao"]').forEach(radio => {
            radio.addEventListener('change', (e) => this.mudarVisualizacao(e.target.value));
        });

        // Carregar obras de exemplo
        this.carregarObras();
        
        // Atualizar clima a cada 30 segundos
        setInterval(() => this.atualizarTodosOsDados(), 30000);
    }

    carregarObras() {
        this.obras = [
            { id: 1, nome: "Obra Centro", lat: -5.7942, lon: -35.2095 },
            { id: 2, nome: "Obra Sul", lat: -5.8200, lon: -35.2100 },
            { id: 3, nome: "Obra Norte", lat: -5.7800, lon: -35.2050 },
            { id: 4, nome: "Obra Leste", lat: -5.8050, lon: -35.1950 }
        ];

        this.atualizarTodosOsDados();
    }

    async atualizarTodosOsDados() {
        const result = await climaManager.buscarClimaObras(this.obras);
        if (result && result.obras) {
            result.obras.forEach(obra => this.adicionarOuAtualizarMarcador(obra));
        }
    }

    adicionarOuAtualizarMarcador(obra) {
        if (this.marcadores[obra.id]) {
            // Atualizar marcador existente
            this.atualizarMarcador(obra);
        } else {
            // Criar novo marcador
            const marker = L.marker([obra.lat, obra.lon])
                .addTo(this.map);
            
            this.marcadores[obra.id] = {
                marker: marker,
                dados: obra
            };
            
            this.atualizarMarcador(obra);
        }
    }

    atualizarMarcador(obra) {
        const marcador = this.marcadores[obra.id];
        if (!marcador) return;

        // Atualizar dados
        marcador.dados = obra;

        // Atualizar popup baseado na visualização ativa
        this.atualizarPopup(marcador);

        // Atualizar cor do ícone
        this.atualizarIconeMarcador(marcador);
    }

    atualizarPopup(marcador) {
        const obra = marcador.dados;
        let conteudo = `<div class="popup-titulo">${obra.nome}</div>`;

        if (this.visualizacaoAtiva === 'temperatura') {
            conteudo += `
                <div class="popup-linha">
                    <span class="popup-label">🌡️ Temperatura:</span>
                    <span class="popup-valor">${obra.temperatura}°C</span>
                </div>
            `;
        } else if (this.visualizacaoAtiva === 'chuva') {
            conteudo += `
                <div class="popup-linha">
                    <span class="popup-label">🌧️ Chuva:</span>
                    <span class="popup-valor">${obra.chuva} mm</span>
                </div>
            `;
        } else if (this.visualizacaoAtiva === 'nuvens') {
            conteudo += `
                <div class="popup-linha">
                    <span class="popup-label">☁️ Nuvens:</span>
                    <span class="popup-valor">${obra.nuvens}%</span>
                </div>
            `;
        }

        marcador.marker.setPopupContent(conteudo);
    }

    atualizarIconeMarcador(marcador) {
        const obra = marcador.dados;
        let cor = this.obterCorTemperatura(obra.temperatura);

        if (this.visualizacaoAtiva === 'chuva') {
            cor = this.obterCorChuva(obra.chuva);
        } else if (this.visualizacaoAtiva === 'nuvens') {
            cor = this.obterCorNuvens(obra.nuvens);
        }

        // Criar ícone customizado
        const html = `
            <div style="
                background-color: ${cor};
                width: 40px;
                height: 40px;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                border: 3px solid white;
                box-shadow: 0 2px 8px rgba(0,0,0,0.2);
                font-size: 18px;
                font-weight: bold;
                color: white;
            ">
                ${this.obterEmoji()}
            </div>
        `;

        const icon = L.divIcon({
            html: html,
            iconSize: [40, 40],
            iconAnchor: [20, 40],
            popupAnchor: [0, -40]
        });

        marcador.marker.setIcon(icon);
    }

    obterEmoji() {
        if (this.visualizacaoAtiva === 'temperatura') return '🌡️';
        if (this.visualizacaoAtiva === 'chuva') return '🌧️';
        if (this.visualizacaoAtiva === 'nuvens') return '☁️';
        return '📍';
    }

    obterCorTemperatura(temp) {
        // Escala: azul (frio) → amarelo (quente) → vermelho (muito quente)
        if (temp < 15) return '#3498db'; // Azul
        if (temp < 20) return '#2ecc71'; // Verde
        if (temp < 25) return '#f1c40f'; // Amarelo
        if (temp < 30) return '#e67e22'; // Laranja
        return '#e74c3c'; // Vermelho
    }

    obterCorChuva(chuva) {
        // Escala de chuva em mm
        if (chuva === 0) return '#95a5a6';      // Cinza (sem chuva)
        if (chuva < 2.5) return '#3498db';      // Azul claro
        if (chuva < 10) return '#2980b9';       // Azul médio
        if (chuva < 50) return '#2471a3';       // Azul escuro
        return '#154360';                       // Azul muito escuro
    }

    obterCorNuvens(nuvens) {
        // Escala de cobertura de nuvens em %
        if (nuvens < 10) return '#3498db';      // Azul claro (céu limpo)
        if (nuvens < 25) return '#5dade2';      // Azul
        if (nuvens < 50) return '#85c1e2';      // Azul claro
        if (nuvens < 75) return '#aed6f1';      // Azul muito claro
        return '#d6eaf8';                       // Azul pálido (muito nublado)
    }

    criarGradienteTemperatura() {
        return {
            frio: '#3498db',
            legal: '#2ecc71',
            quente: '#f1c40f',
            muitoQuente: '#e74c3c'
        };
    }

    mudarVisualizacao(novaVisualizacao) {
        this.visualizacaoAtiva = novaVisualizacao;
        
        // Atualizar todos os marcadores
        Object.values(this.marcadores).forEach(marcador => {
            this.atualizarMarcador(marcador.dados);
        });

        // Atualizar legenda
        this.atualizarLegenda();
    }

    atualizarLegenda() {
        // Criar legenda dinâmica baseada na visualização
        let legenda = document.querySelector('.legenda-temp');
        if (!legenda) {
            legenda = document.createElement('div');
            legenda.className = 'legenda-temp ativo';
            document.body.appendChild(legenda);
        }

        if (this.visualizacaoAtiva === 'temperatura') {
            legenda.innerHTML = `
                <div class="legenda-temp-titulo">Temperatura (°C)</div>
                <div class="legenda-item">
                    <div class="legenda-cor" style="background-color: #3498db;"></div>
                    <span>&lt; 15°C</span>
                </div>
                <div class="legenda-item">
                    <div class="legenda-cor" style="background-color: #2ecc71;"></div>
                    <span>15 - 20°C</span>
                </div>
                <div class="legenda-item">
                    <div class="legenda-cor" style="background-color: #f1c40f;"></div>
                    <span>20 - 25°C</span>
                </div>
                <div class="legenda-item">
                    <div class="legenda-cor" style="background-color: #e67e22;"></div>
                    <span>25 - 30°C</span>
                </div>
                <div class="legenda-item">
                    <div class="legenda-cor" style="background-color: #e74c3c;"></div>
                    <span>&gt; 30°C</span>
                </div>
            `;
        } else if (this.visualizacaoAtiva === 'chuva') {
            legenda.innerHTML = `
                <div class="legenda-temp-titulo">Chuva (mm/h)</div>
                <div class="legenda-item">
                    <div class="legenda-cor" style="background-color: #95a5a6;"></div>
                    <span>Sem chuva</span>
                </div>
                <div class="legenda-item">
                    <div class="legenda-cor" style="background-color: #3498db;"></div>
                    <span>0 - 2.5mm</span>
                </div>
                <div class="legenda-item">
                    <div class="legenda-cor" style="background-color: #2980b9;"></div>
                    <span>2.5 - 10mm</span>
                </div>
                <div class="legenda-item">
                    <div class="legenda-cor" style="background-color: #2471a3;"></div>
                    <span>10 - 50mm</span>
                </div>
                <div class="legenda-item">
                    <div class="legenda-cor" style="background-color: #154360;"></div>
                    <span>&gt; 50mm</span>
                </div>
            `;
        } else if (this.visualizacaoAtiva === 'nuvens') {
            legenda.innerHTML = `
                <div class="legenda-temp-titulo">Nuvens (%)</div>
                <div class="legenda-item">
                    <div class="legenda-cor" style="background-color: #3498db;"></div>
                    <span>0 - 10% (Céu limpo)</span>
                </div>
                <div class="legenda-item">
                    <div class="legenda-cor" style="background-color: #5dade2;"></div>
                    <span>10 - 25% (Pouco nublado)</span>
                </div>
                <div class="legenda-item">
                    <div class="legenda-cor" style="background-color: #85c1e2;"></div>
                    <span>25 - 50% (Parcialmente nublado)</span>
                </div>
                <div class="legenda-item">
                    <div class="legenda-cor" style="background-color: #aed6f1;"></div>
                    <span>50 - 75% (Muito nublado)</span>
                </div>
                <div class="legenda-item">
                    <div class="legenda-cor" style="background-color: #d6eaf8;"></div>
                    <span>&gt; 75% (Totalmente nublado)</span>
                </div>
            `;
        }

        legenda.classList.add('ativo');
    }
}

// Inicializar quando o documento carregar
document.addEventListener('DOMContentLoaded', () => {
    new MapaClima();
});
