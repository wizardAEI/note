## 1. GIS基础
### 1.1 认识GIS
> A geographic information system (GIS) is a system that creates, manages, analyzes, and maps all types of data. GIS connects data to a map, integrating location data (where things are) with all types of descriptive information (what things are like there). This provides a foundation for mapping and analysis that is used in science and almost every industry. GIS helps users understand patterns, relationships, and geographic context. The benefits include improved communication and efficiency as well as better management and decision making.
> -- [esri.com](https://www.esri.com/en-us/what-is-gis/overview)

### 1.2 GIS应用
GIS应用很广泛，在各行各业均有重要作用，如教育行业的地图教学、政府企业资产管理、气象部门气象图等，当然还有农业，我们的耕云也是万万离不开GIS的帮助的。
### 1.3 GIS包含哪些要素
#### 1.3.1 地图数据结构构成

- 矢量数据
   - 点 - Point
   - 线 - LineString
   - 面 - Polygon
   - 多点 - MultiPoint
   - 多线 - MultiLineString
   - 多面 - MultiPolygon
- 栅格数据
   - 瓦片数据等
#### 1.3.2 地图图层

- GIS展示，是通过不同的图层去描述，然后通过图层叠加显示来进行表达的过程
- WebGIS的地图结构：
   - 二维WebGIS的地图结构
      - 栅格底图图层
      - 矢量图层
   - 三维WebGIS的地图结构
      - 地形图层
      - 栅格底图图层
      - 三维模型图层
      - 矢量图层
#### 1.3.3 基础数据结构

- 矢量数据
   - 矢量数据结构是如同X，Y（或者X，Y，Z）坐标，利用点，线，面的形式来表达现实世界
   - 定位明显，属性隐含的特点
   - 数据结构紧凑，冗余度低，表达精度高
- 栅格数据
   - 栅格数据(瓦片模型)是以二维矩阵的形式来表示空间地物或现象分布的数据组织方式，每个矩阵单位称为一个栅格单元(cell)
   - 属性明显，定位隐含的特点
   - 四叉树编码是最有效的栅格数据压缩编码方法之一，还能提高图形操作效率，具有可变的分辨率
#### 1.3.4 常见栅格数据：切片（瓦片）地图

- 瓦片地图金字塔模型是一种多分辨率层次模型，从瓦片金字塔的底层到顶层，分辨率越来越低，但表示的地理范围不变
- 特征：
   - 瓦片分辨率为256 X 256
   - 最小地图等级是0，此时世界地图只由一张瓦片组成
   - 具有唯一的瓦片等级(Z)和瓦片行列坐标编号(X, Y)
   - 瓦片等级越高，组成世界地图的瓦片数越多，可以展示的地图越详细
   - 某一瓦片等级地图的瓦片是由低一级的各瓦片切割成的4个瓦片组成，形成了瓦片金字塔
#### 1.3.5 矢量数据构成：要素 Feature

- 矢量图层内是由多个要素(feature)构成的，要素主要分为点、线、面等类型
- 要素的数据结构
   - 坐标：地理位置，如经度，维度，高度（三维GIS中）构成
   - 样式：表现形式，如图标图片，线条样式，填充色，文字样式等
   - 属性：除经纬度信息之外的关联信息，如名称，地址，电话，面积，长度，备注等
- 坐标信息
   - 点：由经度，维度，高度（三维GIS中）属性组成
   - 线：由多个点组成
   - 面：由一条或多条闭合线组成
- 样式信息
   - 点：符号
   - 线：线型
   - 面：填充
- 属性信息
### 1.4 GIS数据生产

- 测绘
- 无人机航拍
- 手工建模
### 1.5 常见的GIS数据格式
#### 1.5.1 tif - 标签图像文件格式

- tif可以有8位，24位等深度，一般真彩色是24位，地形数据只有一个高度值，采用8位
- 卫星影像数据、地形数据的存储格式都是tif
#### 1.5.2 shp - Shapefile文件时ESRI公司ArcGIS平台的常用格式文件，是工业标准的矢量数据文件

- 1个Shape文件包括三个文件：主文件(.shp)，索引文件(.shx)，dBASE表(.dbf)
- 一个shp文件只能存储点、线、面中的一种类型，不存在混合存在的状态
- shp可以设置很多字段属性
#### 1.5.3 kml/kmz - KML(Keyhold Markup Language，Keyhold标记语言)基于XML的标记语言

- KMZ文件时压缩过的KML文件，不仅包含KML文件，也能包含与之关联的如图片、模型等其他文件
#### 1.5.4 dwg/dxf - AutoCAD的图形文件格式

- dwg文件：AutoCAD的图形文件格式，是二维或三维图形档案，可与dxf文件相互转化
- dxf文件：AutoCAD与其他软件平台之间进行数据交换的一种开放的矢量数据格式
#### 1.5.5 GeoJSON(.json) - 一种开放标准的地理空间数据交换格式
GeoJSON 支持以下几何类型：

- Point
- LineString
- Polygon
- MultiPoint
- MultiLineString
- MultiPolygon

具有附加属性的几何对象为 Feature 对象。 FeatureCollection 对象包含一组要素。
GeoJSON示例：
```json
{ "type": "FeatureCollection",
  "features": [
    { "type": "Feature",
      "geometry": {
        "type": "Point",
        "coordinates": [102.0, 0.5]
        },
        "properties": {
          "prop0": "value0"
        }
      },
    { "type": "Feature",
      "geometry": {
        "type": "LineString",
        "coordinates": [
          [102.0, 0.0], [103.0, 1.0], [104.0, 0.0], [105.0, 1.0]
          ]
        },
      "properties": {
        "prop0": "value0",
        "prop1": 0.0
        }
      },
    { "type": "Feature",
       "geometry": {
         "type": "Polygon",
         "coordinates": [
           [ [100.0, 0.0], [101.0, 0.0], [101.0, 1.0],
             [100.0, 1.0], [100.0, 0.0] ]
           ]
       },
       "properties": {
         "prop0": "value0",
         "prop1": {"this": "that"}
         }
       }
     ]
   }
```
### 1.6 GIS数据存储

- 商业
   - ArcGIS GIS存储引擎，支持Oracle、SQLServer等数据库
- 开源
   - MySQL
   - PostGIS
### 1.7 GIS服务
在网络环境下的一组与地理信息相关的软件功能实体，通过接口暴露封装的GIS功能
常用的GIS服务：

- ArcGIS Server
- GeoServer
- 互联网在线服务，百度、腾讯、高德、天地图等地图服务
### 1.8 GIS开发
常见GIS开发工具和框架

- 商业
   - ArcGIS全家桶
   - 高德、百度、MapBox等SDK
- 开源
   - [Openlayers](https://openlayers.org/)
   - [Leaflet](Leaflet)
   - [MapboxGL](https://www.mapbox.cn/tutorials/gljs/)
   - [Cesium](https://cesium.com/) - 3D
   - [QGIS](https://www.qgis.org/en/site/) - 地图制作，分析等
## 2. QGIS
> A Free and Open Source Geographic Information System

开源GIS系统软件，使用Qt开发
### 2.1 QGIS相关资源

- 官网：[https://www.qgis.org/en/site/](https://www.qgis.org/en/site/)
- GitHub仓库： [https://github.com/qgis/QGIS](https://github.com/qgis/QGIS)
- C++ Api文档： [https://qgis.org/api/3.16/](https://qgis.org/api/3.16/)
- Python Api文档：[https://qgis.org/pyqgis/3.16/](https://qgis.org/pyqgis/3.16/)
- Python Develoer: [https://docs.qgis.org/3.16/en/docs/pyqgis_developer_cookbook/](https://docs.qgis.org/3.16/en/docs/pyqgis_developer_cookbook/)

**可使用Python编写QGIS插件和脚本**
### 2.2 安装

- Windows 下载

[https://download.osgeo.org/osgeo4w/v2/osgeo4w-setup.exe](https://download.osgeo.org/osgeo4w/v2/osgeo4w-setup.exe)

- Mac

[https://qgis.org/downloads/macos/qgis-macos-pr.dmg](https://qgis.org/downloads/macos/qgis-macos-pr.dmg)

