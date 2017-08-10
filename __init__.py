# -*- coding: utf-8 -*-
"""
/***************************************************************************
 BLNImport
                                 A QGIS plugin
 Import .bln files into vector layer
                             -------------------
        begin                : 2017-08-10
        copyright            : (C) 2017 by HEVIN Guillaume
        email                : hevin.guillaume@gmail.com
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load BLNImport class from file BLNImport.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .bln_import import BLNImport
    return BLNImport(iface)
