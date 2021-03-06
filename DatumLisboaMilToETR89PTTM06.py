# -*- coding: utf-8 -*-

"""
***************************************************************************
    DatumLisboaMilToETR89PTTM06.py
    ---------------------
    Date                 : July 2014
    Copyright            : (C) 2014 by Alexander Bruy
    Email                : alexander dot bruy at gmail dot com
***************************************************************************
*                                                                         *
*   This program is free software; you can redistribute it and/or modify  *
*   it under the terms of the GNU General Public License as published by  *
*   the Free Software Foundation; either version 2 of the License, or     *
*   (at your option) any later version.                                   *
*                                                                         *
***************************************************************************
"""

__author__ = 'Alexander Bruy'
__date__ = 'July 2014'
__copyright__ = '(C) 2014, Alexander Bruy'

# This will get replaced with a git SHA1 when you do a git archive

__revision__ = '$Format:%H$'

import os

from PyQt4.QtGui import *

from qgis.core import *

try:
    from processing.parameters.ParameterVector import ParameterVector
    from processing.parameters.ParameterSelection import ParameterSelection
    from processing.outputs.OutputVector import OutputVector
except:
    from processing.core.parameters import ParameterVector
    from processing.core.parameters import ParameterSelection
    from processing.core.outputs import OutputVector

from processing.tools.system import *

from processing.algs.gdal.OgrAlgorithm import OgrAlgorithm
from processing.algs.gdal.GdalUtils import GdalUtils


class DatumLisboaMilToETR89PTTM06(OgrAlgorithm):

    INPUT = 'INPUT'
    OUTPUT = 'OUTPUT'
    GRID = 'GRELHAS'
    GRID_OPTIONS = ['Jose Alberto Goncalves',
                    'Direccao Geral do Territorio']

    def getIcon(self):
        return  QIcon(os.path.dirname(__file__) + '/icons/pttransform.svg')

    def defineCharacteristics(self):
        self.name = 'From Datum Lisboa Militar to ETRS89-PTTM06'
        self.group = 'Vector Datum Transformations'

        self.addParameter(ParameterVector(self.INPUT, 'Input layer',
                          [ParameterVector.VECTOR_TYPE_ANY]))
        self.addParameter(ParameterSelection(self.GRID, 'NTv2 Grid to use (source)',
                          self.GRID_OPTIONS))
        self.addOutput(OutputVector(self.OUTPUT, 'Output layer'))

    def processAlgorithm(self, progress):
        inLayer = self.getParameterValue(self.INPUT)
        conn = self.ogrConnectionString(inLayer)

        output = self.getOutputFromName(self.OUTPUT)
        outFile = output.value

        arguments = ['-s_srs']
        if self.getParameterValue(self.GRID) == 0:
            # Jose Alberto Goncalves
            arguments.append('+proj=tmerc +lat_0=39.66666666666666 +lon_0=1 +k=1 +x_0=200000 +y_0=300000 +ellps=intl +nadgrids=' + os.path.dirname(__file__) + '/grids/ptLX_e89.gsb +wktext +pm=lisbon +units=m +no_defs')
        else:
            # Direccao Geral do Territorio
            arguments.append('+proj=tmerc +lat_0=39.66666666666666 +lon_0=1 +k=1 +x_0=200000 +y_0=300000 +ellps=intl +nadgrids=' + os.path.dirname(__file__) + '/grids/DLX_ETRS89_geo.gsb +wktext +pm=lisbon +units=m +no_defs')
        arguments.append('-t_srs')
        arguments.append('EPSG:3763')
        arguments.append('-f')
        arguments.append('ESRI Shapefile')

        arguments.append(outFile)
        arguments.append(conn)

        commands = ['ogr2ogr', GdalUtils.escapeAndJoin(arguments)]
        GdalUtils.runGdal(commands, progress)
