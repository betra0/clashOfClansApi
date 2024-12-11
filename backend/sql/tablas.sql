


DROP TABLE IF EXISTS `players`;


CREATE TABLE players (
    player_id VARCHAR(12) NOT NULL UNIQUE, -- ID único del jugador (proveniente de la API de Clash of Clans)
    username VARCHAR(50) NOT NULL,        -- Nombre del jugador
    clan_tag VARCHAR(15) NULL,            -- Etiqueta del clan al que pertenece
    role VARCHAR(20) DEFAULT 'member',    -- Rol en el clan (líder, colíder, miembro)
    townhall_level TINYINT UNSIGNED NOT NULL, -- Nivel del Ayuntamiento
    trophies INT UNSIGNED DEFAULT 0,      -- Número de trofeos
    best_trophies INT UNSIGNED DEFAULT 0, -- Máximo de trofeos alcanzados
    ranking INT UNSIGNED DEFAULT 0,       -- Posición en el clan
    donations INT UNSIGNED DEFAULT 0,     -- Tropas donadas
    troops_requested INT UNSIGNED DEFAULT 0, -- Tropas pedidas
    war_stars INT UNSIGNED DEFAULT 0,     -- Estrellas ganadas en guerra
    experience_level INT UNSIGNED DEFAULT 0, -- Nivel de experiencia del jugador
    league VARCHAR(20) NULL,              -- Liga actual del jugador (Cristal, Titanes, etc.)
    attack_count INT UNSIGNED DEFAULT 0,  -- Cantidad de ataques realizados
    defense_count INT UNSIGNED DEFAULT 0, -- Cantidad de defensas realizadas
    status ENUM('active', 'left', 'expelled') DEFAULT 'active', -- Estado del jugador en el clan
    left_date TIMESTAMP NULL DEFAULT NULL, -- Fecha en la que dejó el clan o fue expulsado
    notes TEXT NULL,                      -- Notas adicionales sobre el jugador
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Fecha de registro en tu plataforma
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, -- Última actualización
    PRIMARY KEY (player_id)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;     


CREATE TABLE war (
    startTime TIMESTAMP PRIMARY KEY,
    preparationStartTime TIMESTAMP NOT NULL,
    endTime TIMESTAMP NOT NULL,
    state VARCHAR(50) NOT NULL,
    teamSize INT NOT NULL,
    teamStars INT DEFAULT NULL,
    enemyStars INT DEFAULT NULL,
    attacksPerMember INT NOT NULL,
    enemyClanName VARCHAR(50) DEFAULT NULL,
    enemyClanTag VARCHAR(15) DEFAULT NULL,
    teamAttacks INT DEFAULT NULL,
    enemyAttacks INT DEFAULT NULL,
    teamDestructionPercentage INT DEFAULT NULL,
    enemyDestructionPercentage INT DEFAULT NULL,
    battleModifier VARCHAR(50) DEFAULT NULL
);

CREATE TABLE warMembers (
    warStartTime TIMESTAMP NOT NULL, -- Referencia a la guerra
    player_id VARCHAR(15) NOT NULL, -- Referencia al jugador
    PRIMARY KEY (warStartTime, player_id),
    FOREIGN KEY (warStartTime) REFERENCES war(startTime) ON DELETE CASCADE,
    FOREIGN KEY (player_id) REFERENCES players(player_id) ON DELETE CASCADE
);

CREATE TABLE warAttacks (
    warStartTime TIMESTAMP NOT NULL, -- Referencia a la guerra
    player_id VARCHAR(15) NOT NULL, -- Referencia al jugador
    attackOrder INT NOT NULL, -- Orden del ataque dentro de la guerra
    defenderTag VARCHAR(15) NOT NULL, -- Identificador del objetivo atacado
    stars INT NOT NULL, -- Estrellas ganadas en el ataque
    destructionPercentage INT NOT NULL, -- Porcentaje de destrucción
    duration INT NOT NULL, -- Duración del ataque en segundos
    PRIMARY KEY (warStartTime, player_id, attackOrder),
    FOREIGN KEY (warStartTime, player_id) REFERENCES warMembers(warStartTime, player_id) ON DELETE CASCADE
);