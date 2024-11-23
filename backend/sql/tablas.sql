


DROP TABLE IF EXISTS `players`;



CREATE TABLE players (
    player_id VARCHAR(12) NOT NULL UNIQUE, -- ID único del jugador (proveniente de la API de Clash of Clans)
    username VARCHAR(50) NOT NULL,        -- Nombre del jugador
    clan_tag VARCHAR(15) NULL,            -- Etiqueta del clan al que pertenece
    role VARCHAR(20) DEFAULT 'member',    -- Rol en el clan (líder, colíder, miembro)
    status ENUM('active', 'left', 'expelled') DEFAULT 'active', -- Estado del jugador en el clan
    left_date TIMESTAMP NULL DEFAULT NULL, -- Fecha en la que dejó el clan o fue expulsado
    notes TEXT NULL,                      -- Notas adicionales sobre el jugador
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Fecha de registro en tu plataforma
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, -- Última actualización
    PRIMARY KEY (player_id)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;        