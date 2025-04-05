/*
 Navicat Premium Dump SQL

 Source Server         : yu
 Source Server Type    : MySQL
 Source Server Version : 80403 (8.4.3)
 Source Host           : localhost:3306
 Source Schema         : alumni_db

 Target Server Type    : MySQL
 Target Server Version : 80403 (8.4.3)
 File Encoding         : 65001

 Date: 06/04/2025 00:51:30
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for activities
-- ----------------------------
DROP TABLE IF EXISTS `activities`;
CREATE TABLE `activities`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `description` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `status` int NOT NULL,
  `applicant_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `apply_time` datetime(6) NULL DEFAULT NULL,
  `event_time` datetime(6) NULL DEFAULT NULL,
  `name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `organization` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `phone` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `venue` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 8 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of activities
-- ----------------------------
INSERT INTO `activities` VALUES (2, '一起聚餐呀啦啦啦', 1, 'lisa', '2025-03-10 10:10:31.971414', '2025-02-28 16:00:00.000000', '聚餐', '计算机学院校友会', '10086', '操场');
INSERT INTO `activities` VALUES (3, '一起去读书', 1, 'liaison_bj', '2025-03-10 10:42:56.911006', '2025-03-05 16:00:00.000000', '读书', '北京校友会', '10086', '图书馆');
INSERT INTO `activities` VALUES (5, '一起去看电影', 2, 'liaison_bj', '2025-03-10 10:58:59.576408', '2025-03-05 08:01:00.000000', '看电影', '北京校友会', '10086', '图书馆');
INSERT INTO `activities` VALUES (6, '一起来炒股', 2, 'liaison_finance', '2025-03-10 12:08:47.356465', '2025-03-28 16:00:00.000000', '炒股', '金融行业校友会', '10086', '银行');
INSERT INTO `activities` VALUES (7, '一起cs！', 2, 'liaison_bj', '2025-03-10 14:20:40.727820', '2025-03-06 16:00:00.000000', '上网吧', '北京校友会', '10086', '网吧');

-- ----------------------------
-- Table structure for activities_activityfeedback
-- ----------------------------
DROP TABLE IF EXISTS `activities_activityfeedback`;
CREATE TABLE `activities_activityfeedback`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `rating` double NOT NULL,
  `comment` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `created_at` datetime(6) NOT NULL,
  `activity_id` bigint NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `activities_activityfeedback_activity_id_user_id_99b1d86f_uniq`(`activity_id` ASC, `user_id` ASC) USING BTREE,
  INDEX `activities_activityfeedback_user_id_a5158f7f_fk_users_id`(`user_id` ASC) USING BTREE,
  CONSTRAINT `activities_activityf_activity_id_d8dc7643_fk_activitie` FOREIGN KEY (`activity_id`) REFERENCES `activities` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `activities_activityfeedback_user_id_a5158f7f_fk_users_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of activities_activityfeedback
-- ----------------------------
INSERT INTO `activities_activityfeedback` VALUES (1, 3.5, 'cs太棒了！', '2025-03-23 09:31:31.282993', 7, 3);

-- ----------------------------
-- Table structure for activity_members
-- ----------------------------
DROP TABLE IF EXISTS `activity_members`;
CREATE TABLE `activity_members`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL,
  `activity_id` bigint NOT NULL,
  `status` int NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `user_id`(`user_id` ASC) USING BTREE,
  INDEX `activity_id`(`activity_id` ASC) USING BTREE,
  CONSTRAINT `activity_members_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `activity_members_ibfk_2` FOREIGN KEY (`activity_id`) REFERENCES `activities` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 4 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of activity_members
-- ----------------------------
INSERT INTO `activity_members` VALUES (1, 2, 6, 1);
INSERT INTO `activity_members` VALUES (3, 3, 7, 1);

-- ----------------------------
-- Table structure for activity_participants
-- ----------------------------
DROP TABLE IF EXISTS `activity_participants`;
CREATE TABLE `activity_participants`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `signup_time` datetime(6) NOT NULL,
  `checkin_time` datetime(6) NULL DEFAULT NULL,
  `activity_id` bigint NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `activity_participants_activity_id_7120ea37_fk_activities_id`(`activity_id` ASC) USING BTREE,
  INDEX `activity_participants_user_id_88a99a76_fk_users_id`(`user_id` ASC) USING BTREE,
  CONSTRAINT `activity_participants_activity_id_7120ea37_fk_activities_id` FOREIGN KEY (`activity_id`) REFERENCES `activities` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `activity_participants_user_id_88a99a76_fk_users_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of activity_participants
-- ----------------------------

-- ----------------------------
-- Table structure for alumni_applications
-- ----------------------------
DROP TABLE IF EXISTS `alumni_applications`;
CREATE TABLE `alumni_applications`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `status` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `apply_date` datetime(6) NOT NULL,
  `review_date` datetime(6) NULL DEFAULT NULL,
  `apply_reason` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `reviewer_id` bigint NULL DEFAULT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `alumni_applications_reviewer_id_1645adde_fk_users_id`(`reviewer_id` ASC) USING BTREE,
  INDEX `alumni_applications_user_id_f36f35fa_fk_users_id`(`user_id` ASC) USING BTREE,
  CONSTRAINT `alumni_applications_reviewer_id_1645adde_fk_users_id` FOREIGN KEY (`reviewer_id`) REFERENCES `users` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `alumni_applications_user_id_f36f35fa_fk_users_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of alumni_applications
-- ----------------------------

-- ----------------------------
-- Table structure for alumni_profiles
-- ----------------------------
DROP TABLE IF EXISTS `alumni_profiles`;
CREATE TABLE `alumni_profiles`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `student_id` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `ethnicity` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `gender` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `birth_date` date NULL DEFAULT NULL,
  `education_level` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `major` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `class_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `graduation_date` date NULL DEFAULT NULL,
  `current_company` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `position` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `work_city` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `address` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `is_graduated` int NOT NULL,
  `user_id` bigint NOT NULL,
  `avatar` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `application_status` int NOT NULL,
  `MBTI` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `internship` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `advantage` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `student_id`(`student_id` ASC) USING BTREE,
  UNIQUE INDEX `user_id`(`user_id` ASC) USING BTREE,
  CONSTRAINT `alumni_profiles_user_id_3ed30008_fk_users_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 7 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of alumni_profiles
-- ----------------------------
INSERT INTO `alumni_profiles` VALUES (1, '20011226', '汉族', 'female', NULL, '', '', '计科1班', '2024-03-27', '央国企', '', '', '', 1, 2, 'avatars/avatar_1_1742301154.jpg', 2, 'test', '后端开发', 'java');
INSERT INTO `alumni_profiles` VALUES (2, '20021111', '汉族', 'male', NULL, '', '', '会计1班', '2025-03-28', '公务员', '', '', '', 1, 3, '', 2, 'test', '前端开发', 'vue');
INSERT INTO `alumni_profiles` VALUES (3, '20031111', '壮族', 'female', NULL, '', '', '物联网1班', NULL, '', '', '', '', 0, 4, NULL, 0, 'test', '服务端开发', 'c++');
INSERT INTO `alumni_profiles` VALUES (4, '20101010', '回族', 'male', '2025-03-20', '', '', 'AI1班', '2025-03-28', '银行', '', '', '', 1, 8, '', 2, NULL, '后端开发', 'go');
INSERT INTO `alumni_profiles` VALUES (6, '20101234', '满族', 'female', '2024-03-29', '', '', '通信1班', '2023-03-10', '互联网企业', '', '', '浙江省宁波市江北区', 0, 10, '', 0, NULL, 'UI设计', 'PC');

-- ----------------------------
-- Table structure for association_members
-- ----------------------------
DROP TABLE IF EXISTS `association_members`;
CREATE TABLE `association_members`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `role` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `join_date` date NOT NULL,
  `association_id` bigint NOT NULL,
  `user_id` bigint NOT NULL,
  `status` int NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `association_members_association_id_user_id_b6611086_uniq`(`association_id` ASC, `user_id` ASC) USING BTREE,
  INDEX `association_members_user_id_c36a9a7b_fk_users_id`(`user_id` ASC) USING BTREE,
  CONSTRAINT `association_members_association_id_b38f4e61_fk_associations_id` FOREIGN KEY (`association_id`) REFERENCES `associations` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `association_members_user_id_c36a9a7b_fk_users_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 7 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of association_members
-- ----------------------------
INSERT INTO `association_members` VALUES (1, 'president', '2025-03-03', 1, 1, 0);
INSERT INTO `association_members` VALUES (2, 'member', '2025-03-06', 2, 2, 2);
INSERT INTO `association_members` VALUES (5, 'member', '2025-03-08', 4, 8, 2);
INSERT INTO `association_members` VALUES (6, 'member', '2025-03-08', 2, 8, 1);

-- ----------------------------
-- Table structure for associations
-- ----------------------------
DROP TABLE IF EXISTS `associations`;
CREATE TABLE `associations`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `type` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `description` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `founding_date` date NOT NULL,
  `leader_id` bigint NULL DEFAULT NULL,
  `image` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `associations_name_26ca674c_uniq`(`name` ASC) USING BTREE,
  INDEX `associations_leader_id_08b8ff15_fk_users_id`(`leader_id` ASC) USING BTREE,
  CONSTRAINT `associations_leader_id_08b8ff15_fk_users_id` FOREIGN KEY (`leader_id`) REFERENCES `users` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 5 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of associations
-- ----------------------------
INSERT INTO `associations` VALUES (1, '北京理工大学校友总会', 'general', '北京理工大学校友总会成立于1986年，是在民政部注册的全国性社会团体，是北京理工大学联系和服务全球校友的桥梁和纽带。总会致力于加强校友与母校之间的联系，促进校友之间的交流与合作，支持母校的建设与发展!!!', '1986-05-15', 1, 'association_images/bit.jpg');
INSERT INTO `associations` VALUES (2, '计算机学院校友会', 'college', '计算机学院校友会成立于2000年，致力于促进计算机学院校友之间的交流与合作。本会旨在搭建校友与母校之间的桥梁，定期组织学术讲座、行业交流和校友聚会等活动，为校友提供持续学习和职业发展的平台！', '2000-09-02', 5, 'association_images/1.jpg');
INSERT INTO `associations` VALUES (3, '北京校友会', 'local', '北京校友会是最早成立的地方校友会之一，汇聚了在京工作生活的广大校友。本会定期举办联谊活动、职业发展讲座和公益活动，促进校友之间的互助与合作，同时积极支持母校的发展建设。', '1995-05-15', 6, 'association_images/屏幕截图 2025-02-21 232655.png');
INSERT INTO `associations` VALUES (4, '金融行业校友会', 'industry', '金融行业校友会联结了在金融领域工作的校友，促进行业交流与发展。本会组织金融领域的专业讲座、行业趋势分析和职业发展指导，为金融行业校友提供专业交流平台，同时为在校学生提供实习和就业机会。', '2010-03-20', 7, 'association_images/1.jpg');

-- ----------------------------
-- Table structure for auth_group
-- ----------------------------
DROP TABLE IF EXISTS `auth_group`;
CREATE TABLE `auth_group`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `name`(`name` ASC) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of auth_group
-- ----------------------------

-- ----------------------------
-- Table structure for auth_group_permissions
-- ----------------------------
DROP TABLE IF EXISTS `auth_group_permissions`;
CREATE TABLE `auth_group_permissions`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `auth_group_permissions_group_id_permission_id_0cd325b0_uniq`(`group_id` ASC, `permission_id` ASC) USING BTREE,
  INDEX `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm`(`permission_id` ASC) USING BTREE,
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of auth_group_permissions
-- ----------------------------

-- ----------------------------
-- Table structure for auth_permission
-- ----------------------------
DROP TABLE IF EXISTS `auth_permission`;
CREATE TABLE `auth_permission`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `auth_permission_content_type_id_codename_01ab375a_uniq`(`content_type_id` ASC, `codename` ASC) USING BTREE,
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 57 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of auth_permission
-- ----------------------------
INSERT INTO `auth_permission` VALUES (1, 'Can add log entry', 1, 'add_logentry');
INSERT INTO `auth_permission` VALUES (2, 'Can change log entry', 1, 'change_logentry');
INSERT INTO `auth_permission` VALUES (3, 'Can delete log entry', 1, 'delete_logentry');
INSERT INTO `auth_permission` VALUES (4, 'Can view log entry', 1, 'view_logentry');
INSERT INTO `auth_permission` VALUES (5, 'Can add permission', 2, 'add_permission');
INSERT INTO `auth_permission` VALUES (6, 'Can change permission', 2, 'change_permission');
INSERT INTO `auth_permission` VALUES (7, 'Can delete permission', 2, 'delete_permission');
INSERT INTO `auth_permission` VALUES (8, 'Can view permission', 2, 'view_permission');
INSERT INTO `auth_permission` VALUES (9, 'Can add group', 3, 'add_group');
INSERT INTO `auth_permission` VALUES (10, 'Can change group', 3, 'change_group');
INSERT INTO `auth_permission` VALUES (11, 'Can delete group', 3, 'delete_group');
INSERT INTO `auth_permission` VALUES (12, 'Can view group', 3, 'view_group');
INSERT INTO `auth_permission` VALUES (13, 'Can add content type', 4, 'add_contenttype');
INSERT INTO `auth_permission` VALUES (14, 'Can change content type', 4, 'change_contenttype');
INSERT INTO `auth_permission` VALUES (15, 'Can delete content type', 4, 'delete_contenttype');
INSERT INTO `auth_permission` VALUES (16, 'Can view content type', 4, 'view_contenttype');
INSERT INTO `auth_permission` VALUES (17, 'Can add session', 5, 'add_session');
INSERT INTO `auth_permission` VALUES (18, 'Can change session', 5, 'change_session');
INSERT INTO `auth_permission` VALUES (19, 'Can delete session', 5, 'delete_session');
INSERT INTO `auth_permission` VALUES (20, 'Can view session', 5, 'view_session');
INSERT INTO `auth_permission` VALUES (21, 'Can add 用户', 6, 'add_user');
INSERT INTO `auth_permission` VALUES (22, 'Can change 用户', 6, 'change_user');
INSERT INTO `auth_permission` VALUES (23, 'Can delete 用户', 6, 'delete_user');
INSERT INTO `auth_permission` VALUES (24, 'Can view 用户', 6, 'view_user');
INSERT INTO `auth_permission` VALUES (25, 'Can add 校友信息', 7, 'add_alumniprofile');
INSERT INTO `auth_permission` VALUES (26, 'Can change 校友信息', 7, 'change_alumniprofile');
INSERT INTO `auth_permission` VALUES (27, 'Can delete 校友信息', 7, 'delete_alumniprofile');
INSERT INTO `auth_permission` VALUES (28, 'Can view 校友信息', 7, 'view_alumniprofile');
INSERT INTO `auth_permission` VALUES (29, 'Can add 校友申请', 8, 'add_alumniapplication');
INSERT INTO `auth_permission` VALUES (30, 'Can change 校友申请', 8, 'change_alumniapplication');
INSERT INTO `auth_permission` VALUES (31, 'Can delete 校友申请', 8, 'delete_alumniapplication');
INSERT INTO `auth_permission` VALUES (32, 'Can view 校友申请', 8, 'view_alumniapplication');
INSERT INTO `auth_permission` VALUES (33, 'Can add 校友会', 9, 'add_association');
INSERT INTO `auth_permission` VALUES (34, 'Can change 校友会', 9, 'change_association');
INSERT INTO `auth_permission` VALUES (35, 'Can delete 校友会', 9, 'delete_association');
INSERT INTO `auth_permission` VALUES (36, 'Can view 校友会', 9, 'view_association');
INSERT INTO `auth_permission` VALUES (37, 'Can add 校友会成员', 10, 'add_associationmember');
INSERT INTO `auth_permission` VALUES (38, 'Can change 校友会成员', 10, 'change_associationmember');
INSERT INTO `auth_permission` VALUES (39, 'Can delete 校友会成员', 10, 'delete_associationmember');
INSERT INTO `auth_permission` VALUES (40, 'Can view 校友会成员', 10, 'view_associationmember');
INSERT INTO `auth_permission` VALUES (41, 'Can add 活动', 11, 'add_activity');
INSERT INTO `auth_permission` VALUES (42, 'Can change 活动', 11, 'change_activity');
INSERT INTO `auth_permission` VALUES (43, 'Can delete 活动', 11, 'delete_activity');
INSERT INTO `auth_permission` VALUES (44, 'Can view 活动', 11, 'view_activity');
INSERT INTO `auth_permission` VALUES (45, 'Can add 活动参与者', 12, 'add_activityparticipant');
INSERT INTO `auth_permission` VALUES (46, 'Can change 活动参与者', 12, 'change_activityparticipant');
INSERT INTO `auth_permission` VALUES (47, 'Can delete 活动参与者', 12, 'delete_activityparticipant');
INSERT INTO `auth_permission` VALUES (48, 'Can view 活动参与者', 12, 'view_activityparticipant');
INSERT INTO `auth_permission` VALUES (49, 'Can add 通知', 13, 'add_notification');
INSERT INTO `auth_permission` VALUES (50, 'Can change 通知', 13, 'change_notification');
INSERT INTO `auth_permission` VALUES (51, 'Can delete 通知', 13, 'delete_notification');
INSERT INTO `auth_permission` VALUES (52, 'Can view 通知', 13, 'view_notification');
INSERT INTO `auth_permission` VALUES (53, 'Can add 活动成员', 14, 'add_activitymember');
INSERT INTO `auth_permission` VALUES (54, 'Can change 活动成员', 14, 'change_activitymember');
INSERT INTO `auth_permission` VALUES (55, 'Can delete 活动成员', 14, 'delete_activitymember');
INSERT INTO `auth_permission` VALUES (56, 'Can view 活动成员', 14, 'view_activitymember');

-- ----------------------------
-- Table structure for council_councilmeeting
-- ----------------------------
DROP TABLE IF EXISTS `council_councilmeeting`;
CREATE TABLE `council_councilmeeting`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `content` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `location` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `meeting_time` datetime(6) NOT NULL,
  `invitation_sent` tinyint(1) NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `council_councilmeeting_user_id_3bf6d5fb_fk_users_id`(`user_id` ASC) USING BTREE,
  CONSTRAINT `council_councilmeeting_user_id_3bf6d5fb_fk_users_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 3 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of council_councilmeeting
-- ----------------------------
INSERT INTO `council_councilmeeting` VALUES (2, '第十届计算机学院理事会', '换届了', '大会堂', '2025-03-11 16:00:00.000000', 1, 5);

-- ----------------------------
-- Table structure for council_councilmeeting_invitees
-- ----------------------------
DROP TABLE IF EXISTS `council_councilmeeting_invitees`;
CREATE TABLE `council_councilmeeting_invitees`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `councilmeeting_id` bigint NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `council_councilmeeting_i_councilmeeting_id_user_i_318a9133_uniq`(`councilmeeting_id` ASC, `user_id` ASC) USING BTREE,
  INDEX `council_councilmeeting_invitees_user_id_76ffc1c8_fk_users_id`(`user_id` ASC) USING BTREE,
  CONSTRAINT `council_councilmeeti_councilmeeting_id_465aba49_fk_council_c` FOREIGN KEY (`councilmeeting_id`) REFERENCES `council_councilmeeting` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `council_councilmeeting_invitees_user_id_76ffc1c8_fk_users_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 7 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of council_councilmeeting_invitees
-- ----------------------------
INSERT INTO `council_councilmeeting_invitees` VALUES (4, 2, 2);
INSERT INTO `council_councilmeeting_invitees` VALUES (5, 2, 3);
INSERT INTO `council_councilmeeting_invitees` VALUES (6, 2, 8);

-- ----------------------------
-- Table structure for django_admin_log
-- ----------------------------
DROP TABLE IF EXISTS `django_admin_log`;
CREATE TABLE `django_admin_log`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `object_repr` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `action_flag` smallint UNSIGNED NOT NULL,
  `change_message` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `content_type_id` int NULL DEFAULT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `django_admin_log_content_type_id_c4bce8eb_fk_django_co`(`content_type_id` ASC) USING BTREE,
  INDEX `django_admin_log_user_id_c564eba6_fk_users_id`(`user_id` ASC) USING BTREE,
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_users_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `django_admin_log_chk_1` CHECK (`action_flag` >= 0)
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of django_admin_log
-- ----------------------------

-- ----------------------------
-- Table structure for django_content_type
-- ----------------------------
DROP TABLE IF EXISTS `django_content_type`;
CREATE TABLE `django_content_type`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `model` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `django_content_type_app_label_model_76bd3d3b_uniq`(`app_label` ASC, `model` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 15 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of django_content_type
-- ----------------------------
INSERT INTO `django_content_type` VALUES (11, 'activities', 'activity');
INSERT INTO `django_content_type` VALUES (14, 'activities', 'activitymember');
INSERT INTO `django_content_type` VALUES (12, 'activities', 'activityparticipant');
INSERT INTO `django_content_type` VALUES (1, 'admin', 'logentry');
INSERT INTO `django_content_type` VALUES (8, 'alumni', 'alumniapplication');
INSERT INTO `django_content_type` VALUES (7, 'alumni', 'alumniprofile');
INSERT INTO `django_content_type` VALUES (9, 'association', 'association');
INSERT INTO `django_content_type` VALUES (10, 'association', 'associationmember');
INSERT INTO `django_content_type` VALUES (3, 'auth', 'group');
INSERT INTO `django_content_type` VALUES (2, 'auth', 'permission');
INSERT INTO `django_content_type` VALUES (4, 'contenttypes', 'contenttype');
INSERT INTO `django_content_type` VALUES (13, 'notifications', 'notification');
INSERT INTO `django_content_type` VALUES (5, 'sessions', 'session');
INSERT INTO `django_content_type` VALUES (6, 'users', 'user');

-- ----------------------------
-- Table structure for django_migrations
-- ----------------------------
DROP TABLE IF EXISTS `django_migrations`;
CREATE TABLE `django_migrations`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 36 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of django_migrations
-- ----------------------------
INSERT INTO `django_migrations` VALUES (1, 'contenttypes', '0001_initial', '2025-02-28 16:28:25.915090');
INSERT INTO `django_migrations` VALUES (2, 'contenttypes', '0002_remove_content_type_name', '2025-02-28 16:32:33.147700');
INSERT INTO `django_migrations` VALUES (3, 'auth', '0001_initial', '2025-02-28 16:32:49.917542');
INSERT INTO `django_migrations` VALUES (4, 'auth', '0002_alter_permission_name_max_length', '2025-02-28 16:32:53.585505');
INSERT INTO `django_migrations` VALUES (5, 'auth', '0003_alter_user_email_max_length', '2025-02-28 16:32:53.832495');
INSERT INTO `django_migrations` VALUES (6, 'auth', '0004_alter_user_username_opts', '2025-02-28 16:32:54.053903');
INSERT INTO `django_migrations` VALUES (7, 'auth', '0005_alter_user_last_login_null', '2025-02-28 16:32:54.317409');
INSERT INTO `django_migrations` VALUES (8, 'auth', '0006_require_contenttypes_0002', '2025-02-28 16:32:54.488646');
INSERT INTO `django_migrations` VALUES (9, 'auth', '0007_alter_validators_add_error_messages', '2025-02-28 16:32:54.618835');
INSERT INTO `django_migrations` VALUES (10, 'auth', '0008_alter_user_username_max_length', '2025-02-28 16:32:54.914101');
INSERT INTO `django_migrations` VALUES (11, 'auth', '0009_alter_user_last_name_max_length', '2025-02-28 16:32:55.119999');
INSERT INTO `django_migrations` VALUES (12, 'auth', '0010_alter_group_name_max_length', '2025-02-28 16:32:55.675965');
INSERT INTO `django_migrations` VALUES (13, 'auth', '0011_update_proxy_permissions', '2025-02-28 16:32:56.093430');
INSERT INTO `django_migrations` VALUES (14, 'auth', '0012_alter_user_first_name_max_length', '2025-02-28 16:32:56.228852');
INSERT INTO `django_migrations` VALUES (15, 'users', '0001_initial', '2025-02-28 16:33:15.854764');
INSERT INTO `django_migrations` VALUES (16, 'association', '0001_initial', '2025-02-28 16:33:29.654221');
INSERT INTO `django_migrations` VALUES (17, 'activities', '0001_initial', '2025-02-28 16:33:45.766430');
INSERT INTO `django_migrations` VALUES (18, 'admin', '0001_initial', '2025-02-28 16:34:22.568053');
INSERT INTO `django_migrations` VALUES (19, 'admin', '0002_logentry_remove_auto_add', '2025-02-28 16:34:22.710156');
INSERT INTO `django_migrations` VALUES (20, 'admin', '0003_logentry_add_action_flag_choices', '2025-02-28 16:34:22.780286');
INSERT INTO `django_migrations` VALUES (21, 'alumni', '0001_initial', '2025-02-28 16:34:27.768273');
INSERT INTO `django_migrations` VALUES (22, 'notifications', '0001_initial', '2025-02-28 16:34:32.134357');
INSERT INTO `django_migrations` VALUES (23, 'sessions', '0001_initial', '2025-02-28 16:34:32.854606');
INSERT INTO `django_migrations` VALUES (24, 'alumni', '0002_alumniprofile_avatar_and_more', '2025-03-02 13:40:50.300370');
INSERT INTO `django_migrations` VALUES (25, 'alumni', '0003_alumniprofile_application_status', '2025-03-02 17:20:35.965601');
INSERT INTO `django_migrations` VALUES (26, 'association', '0002_remove_association_parent_and_more', '2025-03-02 22:45:38.829322');
INSERT INTO `django_migrations` VALUES (27, 'association', '0003_remove_associationmember_is_active', '2025-03-02 22:48:24.819856');
INSERT INTO `django_migrations` VALUES (28, 'association', '0004_association_mainimage_association_secondaryimage_and_more', '2025-03-02 23:04:19.934082');
INSERT INTO `django_migrations` VALUES (29, 'association', '0005_remove_association_mainimage_and_more', '2025-03-02 23:13:10.966308');
INSERT INTO `django_migrations` VALUES (30, 'association', '0006_associationmember_status', '2025-03-06 14:38:14.330197');
INSERT INTO `django_migrations` VALUES (31, 'activities', '0002_alter_activity_options_remove_activity_created_at_and_more', '2025-03-10 08:18:16.052161');
INSERT INTO `django_migrations` VALUES (32, 'activities', '0003_activitymember', '2025-03-10 12:11:06.018718');
INSERT INTO `django_migrations` VALUES (33, 'users', '0002_alter_user_role', '2025-03-10 12:40:32.719335');
INSERT INTO `django_migrations` VALUES (34, 'notifications', '0002_notification_status', '2025-03-15 01:18:52.553249');
INSERT INTO `django_migrations` VALUES (35, 'notifications', '0003_remove_notification_created_at', '2025-03-15 03:20:38.583144');

-- ----------------------------
-- Table structure for django_session
-- ----------------------------
DROP TABLE IF EXISTS `django_session`;
CREATE TABLE `django_session`  (
  `session_key` varchar(40) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `session_data` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`) USING BTREE,
  INDEX `django_session_expire_date_a5c62663`(`expire_date` ASC) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of django_session
-- ----------------------------

-- ----------------------------
-- Table structure for donations_donationproject
-- ----------------------------
DROP TABLE IF EXISTS `donations_donationproject`;
CREATE TABLE `donations_donationproject`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `type` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `purpose` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `target_amount` decimal(12, 2) NOT NULL,
  `current_amount` decimal(12, 2) NOT NULL,
  `donor_count` int NOT NULL,
  `end_time` datetime(6) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 11 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of donations_donationproject
-- ----------------------------
INSERT INTO `donations_donationproject` VALUES (1, '图书馆建设基金', '基础设施', '用于图书馆新馆建设和图书采购，提升校园学习环境', 1000000.00, 580000.00, 125, '2024-12-31 23:59:59.000000');
INSERT INTO `donations_donationproject` VALUES (2, '奖学金项目', '助学金', '设立优秀学生奖学金，奖励品学兼优的学生', 500000.00, 320000.00, 89, '2024-09-30 23:59:59.000000');
INSERT INTO `donations_donationproject` VALUES (3, '校园文化建设基金', '文化建设', '支持校园文化活动开展，丰富校园文化生活', 300000.00, 150000.00, 45, '2024-10-31 23:59:59.000000');
INSERT INTO `donations_donationproject` VALUES (4, '创新创业基金', '创业支持', '支持在校学生和校友创新创业项目', 800000.00, 420000.00, 78, '2024-11-30 23:59:59.000000');
INSERT INTO `donations_donationproject` VALUES (5, '实验室设备更新', '教学设施', '更新实验室设备，提升教学质量', 2000000.00, 1200000.00, 156, '2024-12-15 23:59:59.000000');
INSERT INTO `donations_donationproject` VALUES (6, '校友活动中心建设', '基础设施', '建设校友活动中心，为校友提供交流场所', 1500000.00, 680500.00, 236, '2025-06-30 23:59:59.000000');
INSERT INTO `donations_donationproject` VALUES (7, '助困助学基金', '助学金', '资助家庭经济困难的优秀学生完成学业', 600000.00, 450000.00, 167, '2024-08-31 23:59:59.000000');
INSERT INTO `donations_donationproject` VALUES (8, '体育场馆维护基金', '基础设施', '用于维护和更新体育场馆设施', 400000.00, 180000.00, 67, '2024-11-15 23:59:59.000000');
INSERT INTO `donations_donationproject` VALUES (9, '校史馆建设项目', '文化建设', '建设校史馆，传承学校文化', 900000.00, 350000.00, 92, '2025-03-31 23:59:59.000000');
INSERT INTO `donations_donationproject` VALUES (10, '科研创新基金', '学术发展', '支持师生开展创新性科研项目', 1200000.00, 580000.00, 145, '2024-12-31 23:59:59.000000');

-- ----------------------------
-- Table structure for notifications
-- ----------------------------
DROP TABLE IF EXISTS `notifications`;
CREATE TABLE `notifications`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `title` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `content` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `type` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `send_time` datetime(6) NULL DEFAULT NULL,
  `sender_id` bigint NOT NULL,
  `status` int NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `notifications_sender_id_57e62d28_fk_users_id`(`sender_id` ASC) USING BTREE,
  CONSTRAINT `notifications_sender_id_57e62d28_fk_users_id` FOREIGN KEY (`sender_id`) REFERENCES `users` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 8 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of notifications
-- ----------------------------
INSERT INTO `notifications` VALUES (3, '元旦快乐', '吃汤圆了', 'greeting', '2025-03-15 03:25:03.272671', 1, 0);
INSERT INTO `notifications` VALUES (4, '端午快乐', '吃粽子了', 'greeting', '2025-03-15 03:26:10.772352', 1, 0);
INSERT INTO `notifications` VALUES (5, '新年快乐', '过年了', 'greeting', '2025-03-15 03:31:20.264050', 1, 0);
INSERT INTO `notifications` VALUES (6, '中秋快乐', '过中秋吃月饼了', 'activity', '2025-03-15 03:38:08.561379', 5, 0);
INSERT INTO `notifications` VALUES (7, '周杰伦要来', '周杰伦来我们学校唱歌了', 'news', '2025-03-15 03:49:10.726987', 5, 0);

-- ----------------------------
-- Table structure for notifications_receivers
-- ----------------------------
DROP TABLE IF EXISTS `notifications_receivers`;
CREATE TABLE `notifications_receivers`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `notification_id` bigint NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `notifications_receivers_notification_id_user_id_6d755eff_uniq`(`notification_id` ASC, `user_id` ASC) USING BTREE,
  INDEX `notifications_receivers_user_id_a1414b79_fk_users_id`(`user_id` ASC) USING BTREE,
  CONSTRAINT `notifications_receiv_notification_id_120375aa_fk_notificat` FOREIGN KEY (`notification_id`) REFERENCES `notifications` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `notifications_receivers_user_id_a1414b79_fk_users_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 18 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of notifications_receivers
-- ----------------------------
INSERT INTO `notifications_receivers` VALUES (7, 3, 2);
INSERT INTO `notifications_receivers` VALUES (8, 3, 3);
INSERT INTO `notifications_receivers` VALUES (10, 4, 2);
INSERT INTO `notifications_receivers` VALUES (9, 4, 8);
INSERT INTO `notifications_receivers` VALUES (11, 5, 2);
INSERT INTO `notifications_receivers` VALUES (13, 6, 2);
INSERT INTO `notifications_receivers` VALUES (14, 6, 3);
INSERT INTO `notifications_receivers` VALUES (12, 6, 8);
INSERT INTO `notifications_receivers` VALUES (16, 7, 2);
INSERT INTO `notifications_receivers` VALUES (17, 7, 3);
INSERT INTO `notifications_receivers` VALUES (15, 7, 8);

-- ----------------------------
-- Table structure for users
-- ----------------------------
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `password` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `last_login` datetime(6) NULL DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `first_name` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `last_name` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `email` varchar(254) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NULL DEFAULT NULL,
  `role` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `phone` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `gender` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `department` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `graduation_year` int NULL DEFAULT NULL,
  `is_graduated` tinyint(1) NOT NULL,
  `avatar` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `student_id` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `username`(`username` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 11 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of users
-- ----------------------------
INSERT INTO `users` VALUES (1, '123456', NULL, 1, 'admin', '', '', 'admin@example.com', 1, 1, '2025-02-25 20:43:24.000000', 'admin', '', 'male', '', NULL, 0, NULL, '20001012');
INSERT INTO `users` VALUES (2, '123456', NULL, 0, 'dudu', '', '', '', 0, 1, '2025-02-28 16:37:16.571386', 'alumni', '10086', 'male', '计算机学院', NULL, 1, '', '20011226');
INSERT INTO `users` VALUES (3, '123456', NULL, 0, 'dog', '', '', '', 0, 1, '2025-02-28 16:39:43.130560', 'graduated_alumni', '10086', 'male', '经济管理学院', NULL, 1, '', '20021111');
INSERT INTO `users` VALUES (4, '123456', NULL, 0, 'cat', '', '', '', 0, 1, '2025-02-28 16:43:34.187639', 'alumni', '10086', 'male', '信息工程学院', NULL, 0, '', '20031111');
INSERT INTO `users` VALUES (5, '123456', NULL, 0, 'test01', '李', '萨', 'list@example.com', 0, 1, '2025-03-03 20:43:24.000000', 'liaison', '10086', 'female', '经济管理学院', NULL, 0, NULL, '20001111');
INSERT INTO `users` VALUES (6, '123456', NULL, 0, 'liaison_bj', '李', '华', 'liaison_bj@example.com', 0, 1, '2025-03-06 16:59:25.000000', 'liaison', '10086', 'female', '信息工程学院', NULL, 1, NULL, NULL);
INSERT INTO `users` VALUES (7, '123456', NULL, 0, 'liaison_finance', '王', '芳', 'liaison_finance@example.com', 0, 1, '2025-03-06 16:59:25.000000', 'liaison', '10086', 'female', '经济管理学院', NULL, 1, NULL, NULL);
INSERT INTO `users` VALUES (8, '123456', NULL, 0, 'bird', '', '', '', 0, 1, '2025-03-08 05:14:46.751494', 'graduated_alumni', '10086', 'male', '计算机学院', NULL, 1, '', 'test03');
INSERT INTO `users` VALUES (10, '123456', NULL, 0, 'bug', '', '', '', 0, 1, '2025-03-18 11:26:46.914226', 'alumni', '10086', 'male', '信息工程学院', NULL, 0, '', 'test02');

-- ----------------------------
-- Table structure for users_groups
-- ----------------------------
DROP TABLE IF EXISTS `users_groups`;
CREATE TABLE `users_groups`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `users_groups_user_id_group_id_fc7788e8_uniq`(`user_id` ASC, `group_id` ASC) USING BTREE,
  INDEX `users_groups_group_id_2f3517aa_fk_auth_group_id`(`group_id` ASC) USING BTREE,
  CONSTRAINT `users_groups_group_id_2f3517aa_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `users_groups_user_id_f500bee5_fk_users_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of users_groups
-- ----------------------------

-- ----------------------------
-- Table structure for users_user_permissions
-- ----------------------------
DROP TABLE IF EXISTS `users_user_permissions`;
CREATE TABLE `users_user_permissions`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `users_user_permissions_user_id_permission_id_3b86cbdf_uniq`(`user_id` ASC, `permission_id` ASC) USING BTREE,
  INDEX `users_user_permissio_permission_id_6d08dcd2_fk_auth_perm`(`permission_id` ASC) USING BTREE,
  CONSTRAINT `users_user_permissio_permission_id_6d08dcd2_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `users_user_permissions_user_id_92473840_fk_users_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of users_user_permissions
-- ----------------------------

SET FOREIGN_KEY_CHECKS = 1;
