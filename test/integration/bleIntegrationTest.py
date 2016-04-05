#!/usr/bin/env python
###################################################################################
#
# Copyright (c)     2010-2016   Motsai
#
# The MIT License (MIT)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
###################################################################################

import logging
import time
import unittest

from neblina import *
from neblinaBLE import NeblinaBLE, NeblinaDelegate
from neblinaError import *
from neblinaResponsePacket import NebResponsePacket

###################################################################################


def getSuite(deviceAddress):
    BLEIntegrationTest.deviceAddress = deviceAddress
    return unittest.TestLoader().loadTestsFromTestCase(BLEIntegrationTest)

###################################################################################


class BLEIntegrationTest(unittest.TestCase):
    setupHasAlreadyRun = False
    deviceAddress = None

    def setUp(self):
        if not self.deviceAddress:
            logging.warn("No Device Address specified. Skipping.")
            raise unittest.SkipTest

        # Give it a break between each test
        time.sleep(2)

        self.ble = NeblinaBLE()
        self.ble.open(self.deviceAddress)
        if not self.ble.isOpened():
            self.fail("Unable to connect to BLE device.")

        self.ble.setStreamingInterface(Interface.BLE)

    def tearDown(self):
        self.ble.close(self.deviceAddress)

    # def testMotionStreamEuler(self):
    #     self.ble.motionStream(Commands.Motion.EulerAngle, 100)
    #
    # def testMotionStreamIMU(self):
    #     self.ble.motionStream(Commands.Motion.IMU, 100)
    #
    # def testMotionStreamMAG(self):
    #     self.ble.motionStream(Commands.Motion.MAG, 100)
    #
    # def testMotionStreamQuaternion(self):
    #     self.ble.motionStream(Commands.Motion.Quaternion, 100)
    #
    # def testVersion(self):
    #     versions = self.ble.debugFWVersions()
    #     logging.info(versions)
    #     self.assertEqual(versions.apiRelease, 1)
    #     for i in range(0, 2):
    #         self.assertNotEqual(versions.bleFWVersion[i], 255)
    #         self.assertNotEqual(versions.mcuFWVersion[i], 255)
    #
    # def testMEMSComm(self):
    #     logging.debug('Checking communication with the LSM9DS1 chip by getting the temperature...')
    #     temp = self.ble.getTemperature()
    #     logging.info("Board Temperature: {0} degrees (Celsius)".format(temp))
    #
    # def testBattery(self):
    #     batteryLevel = self.ble.getBatteryLevel()
    #     logging.info("Board Battery: {0}\%".format(batteryLevel))
    #
    #
    # def testLEDs(self):
    #     for i in range(0, 100):
    #         self.ble.setLEDs(([0, 1], [1, 0]))
    #         self.ble.setLEDs(([0, 0], [1, 1]))
    #     for i in range(0, 10):
    #         self.ble.setLEDs(([0, 1], [1, 1]))
    #         self.ble.setLEDs(([0, 0], [1, 0]))
    #
    # def testEEPROM(self):
    #     # Verify EEPROM Read/Write limit
    #     with self.assertRaises(AssertionError):
    #         self.ble.EEPROMRead(-1)
    #         self.ble.EEPROMRead(256)
    #         self.ble.EEPROMWrite(-1, "0xFF")
    #         self.ble.EEPROMWrite(256, "0xFF")
    #
    #     # Test Write/Read. Make sure to store current bytes for each page and rewrite it after test.
    #     num = 256
    #     storeBytes = []
    #     # Store EEPROM state
    #     for i in range(0, num):
    #         dataBytes = self.ble.EEPROMRead(i)
    #         storeBytes.append(dataBytes)
    #         logging.debug("EEPROMRead store {0}: {1}".format(i, dataBytes))
    #     # Test write/read
    #     for i in range(0, num):
    #         dataBytes = bytes([i, i, i, i, i, i, i, i])
    #         logging.debug("EEPROMWrite {0} : {1}".format(i, dataBytes))
    #         self.ble.EEPROMWrite(i, dataBytes)
    #     for i in range(0, num):
    #         dataBytes = self.ble.EEPROMRead(i)
    #         logging.debug("EEPROMRead {0} : {1}".format(i, dataBytes))
    #         for j in range(0, 8):
    #             self.assertEqual(dataBytes[j], i)
    #     for i in range(0, num):
    #         logging.debug("EEPROMWrite store {0} : {1}".format(i, storeBytes[i]))
    #         self.ble.EEPROMWrite(i, storeBytes[i])
    #
    # def testMotionDownsample(self):
    #     numPacket = 2
    #     for i in range(1, 51):
    #         factor = i * 20
    #         logging.info("Downsample factor : {0}".format(factor))
    #         self.ble.motionSetDownsample(factor)
    #         start = time.time()
    #         self.ble.motionStream(Commands.Motion.EulerAngle, numPacket)
    #         end = time.time()
    #         self.ble.motionStopStreams()
    #         duration = end - start
    #         logging.info("Downsample factor {0} took {1} seconds".format(factor, duration))
    #         desiredDuration = 1/(1000/factor)*numPacket
    #         #self.assertAlmostEqual(duration, desiredDuration, delta=0.02)
    #
    #     with self.assertRaises(AssertionError):
    #         self.ble.motionSetDownsample(1)
    #         self.ble.motionSetDownsample(1001)
    #     self.ble.motionSetDownsample(20)  # Reset to default
    #
    # def testMotionAccRange(self):
    #     with self.assertRaises(AssertionError):
    #         self.ble.motionSetAccFullScale(-1)
    #         self.ble.motionSetAccFullScale(17)
    #     self.ble.motionSetAccFullScale(2)
    #     self.ble.motionSetAccFullScale(4)
    #     self.ble.motionSetAccFullScale(8)
    #     self.ble.motionSetAccFullScale(16)
    #     self.ble.motionSetAccFullScale(8)   # Reset to default
    #
    # def testMotionState(self):
    #     self.ble.motionStopStreams()
    #     motionState = self.ble.motionGetStates()
    #     self.assertFalse(motionState.distance)
    #     self.assertFalse(motionState.force)
    #     self.assertFalse(motionState.euler)
    #     self.assertFalse(motionState.quaternion)
    #     self.assertFalse(motionState.imuData)
    #     self.assertFalse(motionState.motion)
    #     self.assertFalse(motionState.steps)
    #     self.assertFalse(motionState.magData)
    #     self.assertFalse(motionState.sitStand)
    #     self.assertFalse(motionState.sitStand)
    #
    def testFlashErase(self):
        self.ble.flashErase()
        num = self.ble.flashGetSessions()
        self.assertEqual(num, 0)
        logging.debug("testFlashErase done")

    def testFlashRecord(self):
        self.ble.motionSetDownsample(20)
        self.ble.flashRecord(198, Commands.Motion.Quaternion)
        # self.ble.flashRecord(199, Commands.Motion.IMU)
        # self.ble.flashRecord(200, Commands.Motion.MAG)
        # self.ble.flashRecord(201, Commands.Motion.MAG)

    def testFlashSessionInfo(self):
        packet = self.ble.flashGetSessionInfo(0)
        self.assertEqual(packet.sessionLength, 198)
        # packet = self.ble.flashGetSessionInfo(1)
        # self.assertEqual(packet.sessionLength, 199)
        # packet = self.ble.flashGetSessionInfo(2)
        # self.assertEqual(packet.sessionLength, 200)
        # packet = self.ble.flashGetSessionInfo(3)
        # self.assertEqual(packet.sessionLength, 201)

    # def testFlashSessionPlayback(self):
    #     num = self.ble.flashPlayback(0)
    #     self.assertEqual(num, 198)
    #     # num = self.ble.flashPlayback(1)
    #     # self.assertEqual(num, 199)
    #     # num = self.ble.flashPlayback(2)
    #     # self.assertEqual(num, 200)
    #     # num = self.ble.flashPlayback(3)
    #     # self.assertEqual(num, 201)

    # def testFlashXtreme(self):
    #     first = 100
    #     second = 932000
    #
    #     self.ble.flashErase(Erase.Mass)
    #     self.ble.flashRecord(first, Commands.Motion.Quaternion)
    #     self.ble.flashRecord(second, Commands.Motion.IMU)
    #
    #     num = self.ble.flashGetSessions()
    #     self.assertEqual(num, 2)
    #
    #     num = self.ble.flashPlayback(0)
    #     self.assertEqual(num, first)
    #     num = self.ble.flashPlayback(1)
    #     self.assertEqual(num, second)
    #
    #     packet = self.ble.flashGetSessionInfo(0)
    #     self.assertEqual(packet.sessionLength, first)
    #     packet = self.ble.flashGetSessionInfo(1)
    #     self.assertEqual(packet.sessionLength, second)