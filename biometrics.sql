-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jan 06, 2022 at 02:16 PM
-- Server version: 10.4.22-MariaDB
-- PHP Version: 7.4.27

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `biometrics`
--

-- --------------------------------------------------------

--
-- Table structure for table `administrators`
--

CREATE TABLE `administrators` (
  `id` int(11) NOT NULL,
  `email` varchar(250) NOT NULL,
  `full_names` varchar(250) NOT NULL,
  `phonenumber` varchar(250) NOT NULL,
  `username` varchar(250) NOT NULL,
  `password` varchar(250) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `administrators`
--

INSERT INTO `administrators` (`id`, `email`, `full_names`, `phonenumber`, `username`, `password`) VALUES
(1, 'arashid@kabarak.ac.ke', 'Adam Ahmed Rashid', '0748370216', 'Adam', '$2b$12$Cn3inxvnoc5MMgZRWtATbu01ShKyJRx4LXF2XaBZOADIj8oYLAi6e');

-- --------------------------------------------------------

--
-- Table structure for table `studentattendance`
--

CREATE TABLE `studentattendance` (
  `id` int(11) NOT NULL,
  `template` varchar(250) NOT NULL,
  `time` varchar(250) NOT NULL,
  `fingerprintid` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `studentattendance`
--

INSERT INTO `studentattendance` (`id`, `template`, `time`, `fingerprintid`) VALUES
(48, '<Attendance>: 60 : 2022-01-06 15:25:39 (0, 0)', 'Successfully', 60),
(49, '<Attendance>: 3 : 2022-01-06 15:25:56 (0, 0)', 'Successfully', 3),
(50, '<Attendance>: 60 : 2022-01-06 15:39:40 (0, 0)', 'Successfully', 60),
(51, '<Attendance>: 3 : 2022-01-06 15:42:15 (0, 0)', 'Successfully', 3);

-- --------------------------------------------------------

--
-- Table structure for table `students`
--

CREATE TABLE `students` (
  `id` int(11) NOT NULL,
  `studentname` varchar(250) NOT NULL,
  `admissionnumber` int(11) NOT NULL,
  `admissionnumber1` int(11) NOT NULL,
  `age` varchar(250) NOT NULL,
  `gender` varchar(250) NOT NULL,
  `classgroup` varchar(250) NOT NULL,
  `imagename` varchar(250) NOT NULL,
  `parentname` varchar(250) NOT NULL,
  `parentnumber` varchar(250) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `students`
--

INSERT INTO `students` (`id`, `studentname`, `admissionnumber`, `admissionnumber1`, `age`, `gender`, `classgroup`, `imagename`, `parentname`, `parentnumber`) VALUES
(2, 'sheikh', 3, 123456, '17', 'male', 'form2', '973_3966_1998_20180929_222314.jpg', 'hassan', '+254748370216'),
(3, 'Mohammed Hussein Ali', 60, 3456, '19', 'male', 'form1', '0gkvLzBSGHXJaXEtAFoVlpjWJDD2.jpg', 'Ibtisam Said Swelem', '0722783710'),
(5, 'Hashil Ali', 78, 19778, '19', 'male', 'form4', '973_3966_1998_20180929_222314.jpg', 'Munaa', '0727054516'),
(6, 'Mohammed Ahmed Rashid', 97, 13388, '19', 'male', 'form4', '0gkvLzBSGHXJaXEtAFoVlpjWJDD2.jpg', 'Munaa', '0110077903');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `administrators`
--
ALTER TABLE `administrators`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `studentattendance`
--
ALTER TABLE `studentattendance`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `students`
--
ALTER TABLE `students`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `administrators`
--
ALTER TABLE `administrators`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `studentattendance`
--
ALTER TABLE `studentattendance`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=52;

--
-- AUTO_INCREMENT for table `students`
--
ALTER TABLE `students`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
