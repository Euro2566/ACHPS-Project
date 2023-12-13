-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Dec 13, 2023 at 10:10 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `achps_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `controller`
--

CREATE TABLE `controller` (
  `ConID` int(20) NOT NULL,
  `CropID` int(20) NOT NULL,
  `NitricAcid` text NOT NULL,
  `SunBlock` text NOT NULL,
  `Fan` text NOT NULL,
  `Fogging` text NOT NULL,
  `LED` text NOT NULL,
  `WaterPump` text NOT NULL,
  `NutrientPump` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `controller`
--

INSERT INTO `controller` (`ConID`, `CropID`, `NitricAcid`, `SunBlock`, `Fan`, `Fogging`, `LED`, `WaterPump`, `NutrientPump`) VALUES
(1, 19, 'NO', '75', 'ON', 'ON', 'ON', 'ON', 'OFF'),
(2, 20, 'Yes', '50', 'ON', 'OFF', 'ON', 'ON', 'OFF'),
(3, 24, 'Yes', '50', 'ON', 'OFF', 'ON', 'ON', 'OFF');

-- --------------------------------------------------------

--
-- Table structure for table `crop`
--

CREATE TABLE `crop` (
  `CropID` int(20) NOT NULL,
  `User_id` int(20) NOT NULL,
  `CropName` text NOT NULL,
  `StartDate` text NOT NULL,
  `SN_farm` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `crop`
--

INSERT INTO `crop` (`CropID`, `User_id`, `CropName`, `StartDate`, `SN_farm`) VALUES
(19, 14, 'Farm PK', '10/12/2566', 'F0001'),
(20, 14, 'Farm PB', '10/12/2566', 'F0012'),
(24, 15, 'Farm PB', '10/12/2566', 'F0013');

-- --------------------------------------------------------

--
-- Table structure for table `environment`
--

CREATE TABLE `environment` (
  `EcropID` int(20) NOT NULL,
  `CropID` int(20) NOT NULL,
  `Intensity` int(20) NOT NULL,
  `pH` int(20) NOT NULL,
  `Temperature` int(20) NOT NULL,
  `Humidity` int(20) NOT NULL,
  `Growth` int(20) NOT NULL,
  `EC` int(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `environment`
--

INSERT INTO `environment` (`EcropID`, `CropID`, `Intensity`, `pH`, `Temperature`, `Humidity`, `Growth`, `EC`) VALUES
(12, 19, 100, 120, 35, 60, 0, 65),
(13, 20, 100, 120, 35, 60, 0, 65),
(17, 24, 1000, 6, 40, 65, 0, 1700);

-- --------------------------------------------------------

--
-- Table structure for table `parameter`
--

CREATE TABLE `parameter` (
  `ParaID` int(20) NOT NULL,
  `CropID` int(20) NOT NULL,
  `ECvalue` int(20) NOT NULL,
  `pHvalue` int(20) NOT NULL,
  `IntensityValue` int(20) NOT NULL,
  `TempValue` int(20) NOT NULL,
  `HumiValue` int(20) NOT NULL,
  `ImageResult` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `parameter`
--

INSERT INTO `parameter` (`ParaID`, `CropID`, `ECvalue`, `pHvalue`, `IntensityValue`, `TempValue`, `HumiValue`, `ImageResult`) VALUES
(1, 24, 1112, 6, 1100, 34, 70, 'afsadfgvbfthgdfh'),
(2, 24, 1112, 6, 1100, 34, 70, 'afsadfgvbfthgdfh'),
(3, 19, 1100, 7, 100, 40, 60, 'afsadfgvbfthgdfh');

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `User_id` int(20) NOT NULL,
  `name` text NOT NULL,
  `Email` text NOT NULL,
  `password` text NOT NULL,
  `Phone` text NOT NULL,
  `User_Img` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`User_id`, `name`, `Email`, `password`, `Phone`, `User_Img`) VALUES
(1, 'Watanyu 123', '64015125@kmitl.com', '15152325', '0876837766', 'asdsfdhghfnyuihukhjnm'),
(2, 'Wayu', '45@gmil.com', '123456789asd', '0999999999', 'sdfsdfghdfgjnbmljkh'),
(13, 'Watanyu Wasusirikul', '65015125@kmitl.ac.th', '15325846', '0956400192', 'asdasdfgsdfyertyhfgnfghj'),
(14, 'Watanyu 2000', '66015125@kmitl.ac.th', '15325846asd', '0956400192', 'asdasdfgsdfyertyhfgnfghj'),
(15, 'Watanyu 1999', '67015125@kmitl.ac.th', '15325846asdf', '0956400192', 'asdasdfgsdfyertyhfgnfghj');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `controller`
--
ALTER TABLE `controller`
  ADD PRIMARY KEY (`ConID`);

--
-- Indexes for table `crop`
--
ALTER TABLE `crop`
  ADD PRIMARY KEY (`CropID`);

--
-- Indexes for table `environment`
--
ALTER TABLE `environment`
  ADD PRIMARY KEY (`EcropID`);

--
-- Indexes for table `parameter`
--
ALTER TABLE `parameter`
  ADD PRIMARY KEY (`ParaID`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`User_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `controller`
--
ALTER TABLE `controller`
  MODIFY `ConID` int(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `crop`
--
ALTER TABLE `crop`
  MODIFY `CropID` int(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=25;

--
-- AUTO_INCREMENT for table `environment`
--
ALTER TABLE `environment`
  MODIFY `EcropID` int(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=18;

--
-- AUTO_INCREMENT for table `parameter`
--
ALTER TABLE `parameter`
  MODIFY `ParaID` int(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `User_id` int(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
