# -*- coding: utf-8 -*-
"""
/***************************************************************************
 BLNImport
                                 A QGIS plugin
 Import .bln files into vector layer
                              -------------------
        begin                : 2017-08-10
        git sha              : $Format:%H$
        copyright            : (C) 2017 by HEVIN Guillaume
        email                : hevin.guillaume@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
# Initialize Qt resources from file resources.py
import resources
# Import the code for the dialog
from bln_import_dialog import BLNImportDialog
import os.path


class BLNImport:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'BLNImport_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)


        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&BLN Import')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'BLNImport')
        self.toolbar.setObjectName(u'BLNImport')

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('BLNImport', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        # Create the dialog (after translation) and keep reference
        self.dlg = BLNImportDialog()

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            #self.toolbar.addAction(action)
            try:
                self.iface.layerToolBar().addAction(action)
            except:
                self.iface.addToolBarIcon(action)

        if add_to_menu:
            self.iface.addPluginToVectorMenu(
                self.menu,
                action)
        
        #self._iface.addPluginToVectorMenu(QCoreApplication.translate('EditableGeoCsv', 'Editable GeoCSV'), self.addGeoCsvLayerAction)
        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/BLNImport/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'Import .bln file'),
            callback=self.run,
            parent=self.iface.mainWindow())

	
	

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginVectorMenu(
                self.tr(u'&BLN Import'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar

    def select_input_file(self):
        if self.dlg.Edit.text() == str():
            dialog = QFileDialog(self.dlg)
            dialog.setWindowTitle('Select .bln file:')
            dialog.setNameFilter('*bln')
            dialog.setFileMode(QFileDialog.ExistingFile)
            if dialog.exec_() == QDialog.Accepted:
                filename = dialog.selectedFiles()[0]
            else:
                filename = str()
                
            #we can use : filename = QFileDialog.getOpenFileName(self.dlg, "Select .bln file:","", '*.bln') instead but it didn't remember the last directory openend on my computer (Ubuntu 16.04.2)
            self.dlg.Edit.setText(filename)
        else:
            None

    def run(self):
        """Run method that performs all the real work"""
        
        self.dlg.Edit.clear()
        self.dlg.Button.clicked.connect(self.select_input_file)
        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result:
           #Read de bln file
            path = self.dlg.Edit.text()
            f = open(path , "r")


            bln_file = f.readlines()
            filename = []
            
            f.close()
            
            # Read the name of the file
            
            filename = str()
            l = -5
            letter = path[l]
            while letter != "/":
                filename += letter
                l -= 1
                letter = path[l]
    
            filename = filename[::-1]

            
            nbre_polygon = 1
            nbre_polyline = 1
            
            b = 0
            rd_lines = 0
            
            layer =  QgsVectorLayer("Polygon","","memory")             
            crs = layer.crs().authid()
            
            
            feats_poly = []
            feats_seg = []

            
            
            
            while len(bln_file) > 1 :
                
               
                
                rd_lines, b, name = self.read_data_ligne1(bln_file[0])
                bln_file = bln_file[1:]
                
                x, y = self.read_data(bln_file,rd_lines) 
                bln_file = bln_file[rd_lines:]
                
                
                
                if x[0] ==  x[-1] and y[0] == y[-1]:
                    nbre_polygon, feats_poly = self.save_layer_polygon(x, y, rd_lines, nbre_polygon,crs,feats_poly,name,b)
                    
                
                else:
                    nbre_polyline, feats_seg = self.save_layer_polyline(x, y, rd_lines, nbre_polyline,crs, feats_seg,name,b)
                  
                    
            
            
            if feats_poly != []:
                #Save Polygon
                v_layer_poly = QgsVectorLayer('Polygon?crs=' + crs, filename + "_polygon", "memory")            
                
                prov = v_layer_poly.dataProvider()
                
                prov.addAttributes([QgsField("Number", QVariant.Int),QgsField("Name", QVariant.String),QgsField("Blank", QVariant.Int)])
                v_layer_poly.updateFields()
                
                #values = [QVariant(range(1,nbre_polygon)), QVariant(names_poly)]
                #v_layer_poly.setAttributes(values)
                
                v_layer_poly.startEditing()
                prov.addFeatures(feats_poly)
                v_layer_poly.commitChanges()
     
                QgsMapLayerRegistry.instance().addMapLayer(v_layer_poly)
           
           
           
           
           
            if feats_seg != []:
                v_layer_seg = QgsVectorLayer('LineString?crs=' + crs, filename + "_polyline", "memory")
                prov = v_layer_seg.dataProvider()
                prov.addAttributes([QgsField("Number", QVariant.Int),QgsField("Name", QVariant.String),QgsField("Blank", QVariant.Int)])
                v_layer_seg.updateFields()
                
                v_layer_seg.startEditing()
                prov.addFeatures(feats_seg)
                v_layer_seg.commitChanges()
     
                QgsMapLayerRegistry.instance().addMapLayer(v_layer_seg)
            
            
            
    def read_data_ligne1(self,ligne):        #read data in .bnl file, and append it in list

        name = self.read_attribute(ligne)  #print("firstline ok")

        n_l = str()
        rd_lines = 0
        
        
                
        while ligne[0] == " ":
            ligne = ligne[1:]
        
        deli = ligne.find(',')
        
        if deli == -1:
            deli = ligne.find(' ')
        
        for k in range(0,deli):
            n_l = n_l + ligne[k]
        
        rd_lines = int(n_l)

        
        b = int(ligne[deli+1])

        
        return(rd_lines, b, name)
        
        
        
        
        
    def read_attribute(self,ligne):

        attribute = 0 
        start_attribute = 0
        name = str()
        
        for i in range(0,len(ligne)-1):
            if ligne[i] == '"':
                start_attribute = i+1       #i --> "
                attribute = 1
                break
        
        
        if attribute == 1:
            for i in range(start_attribute,len(ligne)-3):   # last caracter is "/n
                name += ligne[i]
        
        

        return(name)
        
        
        
        
            
    def read_data(self,bln_file, rd_lines):#read points
        
        x = []
        y = []
        
        for k in range(0,rd_lines):
            
            ligne = bln_file[k]
            #print ligne
            x_l = 0
            y_l = 0
            n_l = str()
            
            ######
            #Search x
            ######
            
            while ligne[0] == " ":
                ligne = ligne[1:]
            
            #search delimiter between x and y
            
            deli = ligne.find(',')
        
            if deli == -1:
                deli = ligne.find(' ')
            
            #we read x to the delimiter
            for i in range(0,deli):
                n_l = n_l + ligne[0]
                ligne = ligne[1:]
        
            x_l = float(n_l)
            n_l = str()
            
            #we delete the delimeter
            ligne = ligne[1:]
            
            ######
            #Search y
            ######
                       
            # if there is space between x and y, wee delete
            while ligne[0] == " ":
                ligne = ligne[1:]
            
            #We search if y is the last number of the line (Sometimes bln file have z)
            deli = ligne.find(',')
        
            if deli == -1:
                deli = ligne.find(' ')
            
            if deli == -1:
                deli = len(ligne)
            
            #we read y just like x
            for i in range(0,deli):
                n_l = n_l + ligne[0]
                ligne = ligne[1:]
            
            y_l = float(n_l)

            x.append(x_l)
            y.append(y_l)
            
        return(x,y)
                
       
       
       
       
     
    def save_layer_polygon(self,x, y, rd_lines, nbre_polygon,crs, feats_poly,name,blank):
        
        points = [0]* (rd_lines-1)      #we don't whant the last because = first
        for l in range(0,rd_lines-1):
            points[l] = QgsPoint(x[l],y[l])
            
        layer = QgsVectorLayer('Polygon?crs=' + crs, "","memory")
        
       
        pr = layer.dataProvider()
        pr.addAttributes([QgsField("Polygon", QVariant.Int),QgsField("Name", QVariant.String),QgsField("Blank", QVariant.Int)])
        layer.updateFields()
        
        poly = QgsFeature()    
        poly.setGeometry(QgsGeometry.fromPolygon([points]))
        poly.setAttributes([nbre_polygon, name, blank])
        pr.addFeatures([poly])
       
        feats_poly.append(poly)
       
        nbre_polygon += 1
            
        return(nbre_polygon,feats_poly)
            
            
            
            
    def save_layer_polyline(self,x, y,rd_lines, nbre_polyline,crs, feats_seg,name,blank): 

         
        points = [0]* (rd_lines)      #we don't whant the last because = first
        for l in range(0,rd_lines):
            points[l] = QgsPoint(x[l],y[l])
            
        layer = QgsVectorLayer('LineString?crs=' + crs, "","memory")
        
       
        pr = layer.dataProvider()
        pr.addAttributes([QgsField("Polygon", QVariant.Int),QgsField("Name", QVariant.String),QgsField("Blank", QVariant.Int)])
        layer.updateFields()
        
        seg = QgsFeature()    
        seg.setGeometry(QgsGeometry.fromPolyline(points))
        seg.setAttributes([nbre_polyline, name, blank])
        pr.addFeatures([seg])
       
        feats_seg.append(seg)
       
        nbre_polyline += 1

        
        return(nbre_polyline, feats_seg)
  

   
        
        
            
