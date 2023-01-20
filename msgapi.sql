-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Hôte : localhost
-- Généré le : ven. 20 jan. 2023 à 16:12
-- Version du serveur : 10.4.21-MariaDB
-- Version de PHP : 8.1.6

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données : `msgapi`
--

-- --------------------------------------------------------

--
-- Structure de la table `messages`
--

CREATE TABLE `messages` (
  `msg_id` int(11) NOT NULL,
  `content` text NOT NULL,
  `from_id` int(11) NOT NULL,
  `to_id` int(11) NOT NULL,
  `sendAt` datetime NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Déchargement des données de la table `messages`
--

INSERT INTO `messages` (`msg_id`, `content`, `from_id`, `to_id`, `sendAt`) VALUES
(1, 'Salut! Tu as vu le match hier soir?', 2, 5, '2023-01-20 14:29:36'),
(2, 'Oui, c\'était incroyable! J\'ai adoré la façon dont ils ont joué.', 5, 2, '2023-01-20 14:35:49'),
(3, 'Salut! Tu as vu le match hier soir?', 2, 4, '2023-01-20 14:38:44'),
(4, 'J\'ai été vraiment impressionnée par le jeu de l\'attaquant. Il a marqué deux buts!', 5, 2, '2023-01-20 14:39:53');

-- --------------------------------------------------------

--
-- Structure de la table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `fullname` varchar(100) NOT NULL,
  `username` varchar(50) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(200) NOT NULL,
  `img_link` text DEFAULT NULL,
  `bio` text DEFAULT NULL,
  `createdAt` datetime NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Déchargement des données de la table `users`
--

INSERT INTO `users` (`id`, `fullname`, `username`, `email`, `password`, `img_link`, `bio`, `createdAt`) VALUES
(2, 'brou kouadio stephane fabien', 'fabien', 'fabienbrou99@gmail.com', '$2b$12$zkSP9F1k65mZ4dai8SjAm.0qk0PwJ70zrwxrfEHasV.7aMt3o5Du2', 'https://avataaars.io/?avatarStyle=Circle&topType=ShortHairShortFlat&accessoriesType=Blank&hairColor=Black&facialHairType=Blank&clotheType=CollarSweater&clotheColor=Gray02&eyeType=Happy&eyebrowType=Angry&mouthType=Disbelief&skinColor=Pale', 'I\'m a kind and generous person who always puts others before himself. He is a hard worker and loves to help those in need. He is a great listener and is always willing to lend a helping hand. He is a great friend and an even better person', '2023-01-20 13:37:35'),
(3, 'karen smith', 'karen', 'karensmith@gmail.com', '$2b$12$f/sjk4bNe2yvG0Rlylb/jOdf9MiVeAMB4CSkjcjtfhEHj3ke/gtOK', 'https://avataaars.io/?avatarStyle=Circle&topType=LongHairStraight&accessoriesType=Prescription02&hairColor=Auburn&facialHairType=MoustacheFancy&facialHairColor=BrownDark&clotheType=BlazerShirt&clotheColor=PastelOrange&eyeType=Cry&eyebrowType=UnibrowNatural&mouthType=Tongue&skinColor=Light', 'I\'m a friendly and outgoing person who loves to meet new people. I\'m a creative thinker and I\'m always looking for new ways to solve problems. I\'m passionate about helping others and I\'m always willing to lend a helping hand. I\'m a great listener and I\'m always open to new ideas and perspectives.', '2023-01-20 13:54:22'),
(4, 'rosa mendez lopez', 'rosa', 'rosa.mendez@gmail.com', '$2b$12$VtCIFBLeqV264OHEPrUI2OFpRx3fpEu9kmIni0yL0fImDL5kaniiG', 'https://avataaars.io/?avatarStyle=Circle&topType=LongHairStraight2&accessoriesType=Prescription02&hairColor=BrownDark&facialHairType=BeardLight&facialHairColor=BrownDark&clotheType=GraphicShirt&clotheColor=PastelOrange&eyeType=Wink&eyebrowType=SadConcerned&mouthType=Smile&skinColor=Light', 'I\'m a friendly and outgoing person who loves to meet new people. I\'m a creative thinker and I\'m always looking for new ways to solve problems. I\'m passionate about helping others and I\'m always willing to lend a helping hand. I\'m a great listener and I\'m always open to new ideas and perspectives.', '2023-01-20 13:54:42'),
(5, 'danielle johnson', 'danielle', 'daniellejohnson@gmail.com', '$2b$12$ltWZhQYxc/fbbXyuu96vq.xJ4KcogL7kEzHMkEXYyu2.E3.6obR.O', 'https://avataaars.io/?avatarStyle=Circle&topType=LongHairStraight2&accessoriesType=Round&hairColor=BrownDark&facialHairType=Blank&clotheType=Hoodie&clotheColor=Gray02&eyeType=Close&eyebrowType=SadConcerned&mouthType=Smile&skinColor=Light', 'I\'m a friendly and outgoing person who loves to meet new people. I\'m a creative thinker and I\'m always looking for new ways to solve problems. I\'m passionate about helping others and I\'m always willing to lend a helping hand. I\'m a great listener and I\'m always open to new ideas and perspectives.', '2023-01-20 13:55:57');

--
-- Index pour les tables déchargées
--

--
-- Index pour la table `messages`
--
ALTER TABLE `messages`
  ADD PRIMARY KEY (`msg_id`),
  ADD KEY `from_id` (`from_id`),
  ADD KEY `to_id` (`to_id`);

--
-- Index pour la table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT pour les tables déchargées
--

--
-- AUTO_INCREMENT pour la table `messages`
--
ALTER TABLE `messages`
  MODIFY `msg_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT pour la table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- Contraintes pour les tables déchargées
--

--
-- Contraintes pour la table `messages`
--
ALTER TABLE `messages`
  ADD CONSTRAINT `messages_ibfk_1` FOREIGN KEY (`from_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `messages_ibfk_2` FOREIGN KEY (`to_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
