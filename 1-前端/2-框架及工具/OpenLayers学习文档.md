# OpenLayers 学习文档

## 前导

### GIS

#### 地图数据的结构

矢量数据

- 点 point
- 线 lineString
- 面 polygon
- 多点
- 多线
- 多面

栅格数据

- 瓦片数据

## Quick Start

### [Accessible Map (openlayers.org)](https://openlayers.org/en/latest/examples/accessible.html)

#### 注意点

`package.json`修改：

```json
{
  "name": "projectname"
  "version": "1.0.0",
  "description": "",
  "main": "main.js",
  "dependencies": {
    "ol": "^6.9.0"
  },
  "devDependencies": {
    "parcel-bundler": "^1.12.5"
  },
  "scripts": {
    "start": "parcel index.html",
    "build": "parcel build --public-url . index.html"
  }
}
```

关于`ol/ol.css`的问题：如果报了找不到`ol.css`的错误，可以直接去 node_modules 里去找`ol.css`然后放到 html 文件的 style 里

#### 学习目标

- Map 函数内的相关参数的意义
- 如何在 vue 上使用

### Map 函数中的基本参数：

#### target：

确定地图要绑定的 element（通过寻找 ID 来绑定）

#### View：

View 用来控制地图实例的一些特性

```javascript
view: new View({
                center: proj.fromLonLat([37.41, 8.82]), //地图中心，可以采用多种定位方式
                zoom: 8,//放大倍数
                rotation: 0,//旋转角度
            }),
```

其中还有个`projection`参数不太清楚意思，先把原放在这：

A `View` also has a `projection`. The projection determines the coordinate system of the `center` and the units for map resolution calculations. If not specified (like in the above snippet), the default projection is Spherical Mercator (EPSG:3857), with meters as map units.

#### Source

用来设定一个 layer 的远程数据源

数据源在包内对应的数据是：`ol/source/OSM`

#### Layer

Layer 是对数据可视化的画板

ol 的 layer 大致有 4 种形式：

- `ol/layer/Tile` - Renders sources that provide tiled images in grids that are organized by zoom levels for specific resolutions.
- `ol/layer/Image` - Renders sources that provide map images at arbitrary extents and resolutions.
- `ol/layer/Vector` - Renders vector data client-side.
- `ol/layer/VectorTile` - Renders data that is provided as vector tiles.

### ol/Map

Map 是 OpenLayers 中核心的部分，官网中对于它需包含的属性有这样的介绍： For a map to render, a view, one or more layers, and a target container are needed

Map 的方法合集： [OpenLayers v6.9.0 API - Class: Map](https://openlayers.org/en/latest/apidoc/module-ol_Map-Map.html)
Map 中的 View 方法合集： [OpenLayers v6.9.0 API - Class: View](https://openlayers.org/en/latest/apidoc/module-ol_View-View.html)

### ol/source/XYZ

XYZ 图层源， projection 默认为 EPSG:3857

在本项目中，使用到的 XYZ 图层源为世界地图的图层源。EPSG:3857

### proj.transform

将该投影源下的坐标转换为目标投影下的对应坐标并返回，且并不会改变原坐标。

```javascript
proj.transform(target.coordinate, 'EPSG:3857', 'EPSG:4326')
```

这个函数的作用是将目标点的坐标（从伪墨卡托投影）转换为了经纬度坐标（EPSG:4326 为常用的地理坐标系）

## 功能实现：

### 设置需要渲染的 DOM 目标（通过 id）：

```javascript
map.setTarget('map')
```

### 新增图层

```javascript
let cityNameLayer = new TileLayer({
  source: new XYZ({
    url:
      'https://t' +
      Math.round(Math.random() * 7) +
      '.tianditu.gov.cn/DataServer?T=cva_w&x={x}&y={y}&l={z}&tk=7e2ced6843b376a14f69a9f5885d3d2d',
    crossOrigin: 'anonymous',
  }),
})
map.addLayer(cityNameLayer)
```

### 新增一个 Vector 图层

```javascript
//新建source，并设置默认样式
let cameraSource = new VectorSource({
  wrapX: false,
  style: new Style({
    stroke: new Stroke({
      color: "rgba(0,0,0,0)",
      width: 2,
    }),
  }),
});

//新建layer，并设置zIndex
let cameraVectorLayer = new VectorLayer({
  source: cameraSource,
});
cameraVectorLayer.setZIndex(9);

//统计feature
let cameraMaker = new Feature({
    geometry: ...,
    id: ...,
    departmentId: ...,
    enterpriseId: ...,
    name: ...,
    seriesNum: ...,
    verifyCode: ...,
    camer: ...,
});
//feature的额外设置
cameraMaker.setId(...);
let cameraStyle = new Style({
    image: new OlIcon({
        src: ...,
    }),
});
cameraMaker.setStyle(cameraStyle);

//填充到feature集合中
cameraMarkerAll.push(camersMarker);


//且source添加feature集合
cameraSource.addFeatures([...cameraMarkerAll]);

//添加图层
map.addLayer(cameraVectorLayer);
```

### 新增一个 WMS 图层

[Single Image WMS (openlayers.org)](https://openlayers.org/en/latest/examples/wms-image.html)

对应的 Vue 写法：

```vue
<template>
  <div id="map" class="map"></div>
</template>

<script>
import olMap from 'ol/Map'
import ImageLayer from 'ol/layer/Image'
import TileLayer from 'ol/layer/Tile'
import View from 'ol/View'
import { OSM, ImageWMS } from 'ol/source'
import { onMounted } from 'vue'

export default {
  name: 'olWMSExample',
  setup() {
    const layers = [
      new TileLayer({
        source: new OSM(),
      }),
      new ImageLayer({
        extent: [-13884991, 2870341, -7455066, 6338219],
        source: new ImageWMS({
          url: 'https://ahocevar.com/geoserver/wms',
          params: { LAYERS: 'topp:states' },
          ratio: 1,
          serverType: 'geoserver',
        }),
      }),
    ]
    const map = new olMap({
      layers: layers,
      view: new View({
        center: [-10997148, 4569099],
        zoom: 4,
      }),
    })
    onMounted(() => {
      map.setTarget('map')
    })
  },
}
</script>

<style>
.map {
  width: 100%;
  height: 400px;
}
</style>
```

### 使用 WMS 的瓦片图层

```javascript
const tileLayer = new TileLayer({
  extent: [-13884991, 2870341, -7455066, 6338219],
  source: new TileWMS({
    url: 'https://ahocevar.com/geoserver/wms',
    params: { LAYERS: 'topp:states', TILED: true },
    serverType: 'geoserver',
    transition: 0,
  }),
})
map.addLayer(tileLayer)
```

### 禁止地图拖动

```javascript
import DragPan from 'ol/interaction/DragPan'

map.getInteractions().forEach(element => {
  if (element instanceof DragPan) element.setActive(false)
})
```

### 将地图限制到中国范围内

```javascript
map.setView(
  new View({
    center: [-10997148, 4569099],
    zoom: 4,
    extent: proj.transformExtent([70, 3, 140, 55], 'EPSG:4326', 'EPSG:3857'), //这里的这个要看一下是否要转换，如果用的layer本来就是4326，就不用转换了
  })
)
```

### 显示图例，显示当前可视区中的对应人口密度图例

```javascript
	setup() {
		   const tileLayer = new TileLayer({
                extent: [-13884991, 2870341, -7455066, 6338219],
                source: wmsSource
            })
            const layers = [
                new TileLayer({
                    source: new OSM({
                        wrapX: false
                    }),
                })
            ]
            const map = new olMap({
                layers: layers,
            })
            map.addLayer(tileLayer)
            map.setView(new View({
                center: [-10997148, 4569099],
                zoom: 4,
            }))
            var getExtent = function () {
            return map.getView().calculateExtent()
            }
            var getProjectionCode = function () {
                return map.getView().getProjection().getCode()
            }
            var updateLegend = function(resolution) {
                var graphicUrl = wmsSource.getLegendUrl(resolution);
                const crs = `&CRS=${getProjectionCode()}`;
                const bbox = `&BBOX=${getExtent().join(',')}`
                const height = getHeight(getExtent())
                const width = getWidth(getExtent())
                const heightAndWidth = `&srcwidth=${height}&srcheight=${width}`
                const legenOptions = "&legend_options=countMatched:true;fontAntiAliasing:true;hideEmptyRules:true;forceLabels:on"
                console.log(`${graphicUrl}${crs}${bbox}${heightAndWidth}${legenOptions}`);
            };


            onMounted(() => {
                map.setTarget('map')
                console.log(wmsSource.getLegendUrl(map.getView().getResolution()))
                map.on('click', () => {
                    updateLegend(map.getView().getResolution())
                })
                })
       }
```

### 获取世界地图对应时区的时间

[WMS Time (openlayers.org)](https://openlayers.org/en/latest/examples/wms-time.html)

### 在有 WMS 的视图上鼠标变成 pointer

```javascript
map.on('pointermove', function (evt) {
  if (evt.dragging) {
    return
  }
  const pixel = map.getEventPixel(evt.originalEvent)
  const hit = map.forEachLayerAtPixel(pixel, function (e) {
    console.log(e)
    //判断当前pixel下是否有指定的图层，一旦有，返回true
    if (e.className_ == wmsLayer.getClassName()) return true
    return false
  })
  map.getTargetElement().style.cursor = hit ? 'pointer' : ''
})
```

注意这里的`map.forEachLayerAtPixel`,这个函数的第二个参数是一个 callback，当这个函数返回 false 的时候，`map.forEachLayerAtPixel`会继续执行往下找，如果返回 true 则直接停止查找

### 判断当前位置下，某个 source 的信息（WMS）

```javascript
map.on('singleclick', event => {
  const pixel = map.getEventPixel(event.originalEvent)
  const hit = map.forEachLayerAtPixel(pixel, e => {
    if (e.className_ == farmLayer.getClassName()) return true
    return false
  })
  if (hit) {
    const url = source.getFeatureInfoUrl(
      event.coordinate,
      map.getView().getResolution(),
      'EPSG:4326',
      { INFO_FORMAT: 'application/json' }
    )
    if (url) {
      fetch(url)
        .then(res => res.text())
        .then(body => {
          console.log(JSON.parse(body))
        })
    }
  }
})
```

### 请求 WMS 的 source 中的 feature 数据的过程

1. 获取请求数据的链接

   ```javascript
   const url = source.getFeatureInfoUrl(
     event.coordinate,
     map.getView().getResolution(),
     'EPSG:4326',
     { INFO_FORMAT: 'application/json' }
   )
   ```

2. fetch 请求数据，这里是 json 形式的数据，所以还要转成 json 的

   ```javascript
   fetch(url)
     .then(res => res.text())
     .then(body => {
       body = JSON.parse(body) //JSON数据解析
     })
   ```

### 通过获取的 geometry（WMS 服务中的）信息来创建 VectorLayer

一般 geometry 在返回的数据的 features 里存储，如果返回的 geometry 是这样的：

```json
{
	type: 'Polygon',
	coordinates:[Array(23)]
}
```

那么我们可以这样创建：

```javascript
pointerLayer = new VectorLayer({
  source: new VectorSource({
    features: [
      new Feature({
        //注意这里new的是 Polygon
        geometry: new Polygon(body.features[0]['geometry']['coordinates']),
      }),
    ],
  }),
})
//给layer添加样式
pointerLayer.setStyle(
  new Style({
    stroke: new Stroke({
      color: '#00ffff',
      width: 1,
    }),
    fill: new Fill({
      color: 'rgba(0,255,255,0.2)',
    }),
  })
)
map.addLayer(pointerLayer)
```

### 在地图上画画

[Icon Colors (openlayers.org)](https://openlayers.org/en/latest/examples/icon-color.html)

```javascript
/**
 * @param {Map} map 地图
 * @description 地图上划分地块
 */
const drawOnMap = map => {
  const source = new VectorSource({})
  const vector = new VectorLayer({
    source: source,
    style: new Style({
      fill: new Fill({
        color: 'rgba(255, 255, 255, 0.2)',
      }),
      stroke: new Stroke({
        color: '#224b8f',
        width: 2,
      }),
      image: new CircleStyle({
        radius: 7,
        fill: new Fill({
          color: '#224b8f',
        }),
      }),
    }),
  })
  map.addLayer(vector)

  const modify = new Modify({ source: source })
  const draw = new Draw({ source: source, type: 'Polygon' })

  map.addInteraction(modify)
  map.addInteraction(draw)
  const snap = new Snap({ source: source })
  map.addInteraction(snap)
  // map.removeInteraction(modify)
  // map.removeInteraction(draw)
  // map.removeInteraction(snap)
}
drawOnMap(map)
```

### 其他

```vue
<!--
 * @Author: wangDeJiang(aei)
 * @Date: 2021-12-14 09:37:45
 * @LastEditors: wangDeJiang(aei)
 * @LastEditTime: 2021-12-14 16:26:14
 * @Description: 一个美国地图一个世界地图，在触碰到国家时手型变化，点击位置后获取该位置值
-->
<template>
  <div id="map" class="map"></div>
  <div id="info">&nbsp;</div>
</template>

<script>
import ImageLayer from 'ol/layer/Image'
import ImageWMS from 'ol/source/ImageWMS'
import Map from 'ol/Map'
import View from 'ol/View'
import { onMounted } from 'vue'
// import VectorLayer from 'ol/layer/Vector';

import TileLayer from 'ol/layer/Tile'
import { TileWMS } from 'ol/source'

export default {
  name: 'olWMSExample',
  setup() {
    const wmsSource = new ImageWMS({
      url: 'https://ahocevar.com/geoserver/wms',
      params: { LAYERS: 'ne:ne' },
      serverType: 'geoserver',
      crossOrigin: 'anonymous',
    })
    const wmsLayer = new ImageLayer({
      source: wmsSource,
      className: 'Imagehhhhhh',
    })
    const view = new View({
      center: [0, 0],
      zoom: 1,
    })
    const map = new Map({
      layers: [wmsLayer],
      view: view,
    })

    onMounted(() => {
      map.setTarget('map')
      map.on('singleclick', function (evt) {
        console.log(evt.map.getLayers())
        document.getElementById('info').innerHTML = ''
        const viewResolution = view.getResolution()
        const url = wmsSource.getFeatureInfoUrl(
          evt.coordinate,
          viewResolution,
          'EPSG:3857',
          { INFO_FORMAT: 'text/html' }
        )
        if (url) {
          fetch(url)
            .then(response => {
              // console.log(response)
              return response.text()
            })
            .then(html => {
              document.getElementById('info').innerHTML = html
            })
        }
      })

      map.addLayer(
        new TileLayer({
          extent: [-13884991, 2870341, -7455066, 6338219],
          source: new TileWMS({
            url: 'https://ahocevar.com/geoserver/wms',
            params: { LAYERS: 'topp:states', TILED: true },
            serverType: 'geoserver',
            transition: 0,
          }),
        })
      )

      map.on('pointermove', function (evt) {
        if (evt.dragging) {
          return
        }
        const pixel = map.getEventPixel(evt.originalEvent)
        const hit = map.forEachLayerAtPixel(pixel, function (e) {
          if (e.className_ == wmsLayer.getClassName()) return true
          return false
        })
        map.getTargetElement().style.cursor = hit ? 'pointer' : ''
      })
    })
  },
}
</script>

<style>
.map {
  width: 100vw;
  height: 400px;
}
</style>
```

## 名词解释：

### 栅格切片

可以简单的理解成：将地图图片切割成分片根据需要显示地图的需要来加载地图切片。

### vector tile 矢量切片

[矢量切片（Vector Tile）*不睡觉的怪叔叔的博客-CSDN 博客*矢量切片](https://blog.csdn.net/qq_35732147/article/details/89352283)

### Web Mercator 坐标系

[墨卡托及 Web 墨卡托投影\_shellching 的专栏-CSDN 博客\_web 墨卡托投影](https://blog.csdn.net/shellching/article/details/79627653)

### WGS84 坐标系

[什么是 WGS84 坐标系 - 知乎 (zhihu.com)](https://zhuanlan.zhihu.com/p/97363931)

EPSG:4326 对应 WGS85 坐标系

### 瓦片，WMS，WMTS

[瓦片、WMS 与 WMTS\_潘达小新-CSDN 博客\_wms wmts](https://blog.csdn.net/fangyu723/article/details/103958613)

### EPSG:3857 和 EPSG:4326

[地理信息 epsg:4326 和 epsg:3857\_了不起的卡卡丘丶的博客-CSDN 博客\_epsg:4326](https://blog.csdn.net/qq_37891961/article/details/104704020)

[GIS 基础知识 - 坐标系、投影、EPSG:4326、EPSG:3857 - \__熊_ - 博客园 (cnblogs.com)](https://www.cnblogs.com/E7868A/p/11460865.html)

# Turf.js 学习文档

## 基本文档

[Turf.js 中文网 (fenxianglu.cn)](https://turfjs.fenxianglu.cn/)

[Turf.js | Advanced geospatial analysis (turfjs.org)](https://turfjs.org/)

## 快速实现拆分合并功能的例子

[基于 Turf.js 教你快速实现地理围栏的合并拆分\_腾讯位置服务-CSDN 博客\_turf 合并](https://blog.csdn.net/weixin_45628602/article/details/106139207)

[leaflet 结合 turf.js 实现多边形分割(附源码下载) - GIS 之家 - 博客园 (cnblogs.com)](https://www.cnblogs.com/giserhome/archive/2020/01/07/12161278.html)

## 拆分规划

#### 线拆分多边形（无缝隙）

1. 拆分多边形为线 使用到 API 为：polygonToLine 注意转换为线段的时候，多边形会随机找一个地方断开

2. 计算多边形的线与分割线之间的交点，并返回交点数 使用到 API 为：lineIntersect

![1639703081884](https://aeiblog-1301396258.cos.ap-chengdu.myqcloud.com/img/1639703081884.png)

3. 如果返回的交点数大于 2，则返回分割错误，否则继续

如以下情况则返回错误：

![1639703191455](https://aeiblog-1301396258.cos.ap-chengdu.myqcloud.com/img/1639703191455.png)![1639703227944](https://aeiblog-1301396258.cos.ap-chengdu.myqcloud.com/img/1639703227944.png)

4. 进行线段间切割,互相切割，最终得到切后线段。使用到的 API：lineSplit

![1639703574440](https://aeiblog-1301396258.cos.ap-chengdu.myqcloud.com/img/1639703574440.png)![1639705279898](https://aeiblog-1301396258.cos.ap-chengdu.myqcloud.com/img/1639705279898.png)![1639705439462](https://aeiblog-1301396258.cos.ap-chengdu.myqcloud.com/img/1639705439462.png)

**注意！！！**在这里直接用线切割会造成精度被限制而导致切割后的点有偏差，最终连不成一条线。为了避免这个问题，我们要把问题转换成**用点切线**，即最开始我们使用第 2 步中的交点，分别对线切割，而不是用线直接切割。这样就解决了偏差问题。创建点集的方法：multiPoint

5. 将线段拼接成多边形 使用到的 API ： polygonize

![1639705622370](https://aeiblog-1301396258.cos.ap-chengdu.myqcloud.com/img/1639705622370.png)

具体方法是，先将线段存为线段集合，再进行拼接，用到的 API：combine

我们按编号组成线集合并拼接成平面。大功告成！

#### 线段拆分多边形（有缝隙，目前在用的方法）

1. 将 sliceLine 加粗，使用 API：buffer

![1639726125391](https://aeiblog-1301396258.cos.ap-chengdu.myqcloud.com/img/1639726125391.png)

![1639726386543](https://aeiblog-1301396258.cos.ap-chengdu.myqcloud.com/img/1639726386543.png)

1. 将待划分的多边形简单化（去除扭结点），使用 API：unkinkPolygon
2. 使用加粗的 sliceLine 裁剪多边形，使用 API：difference

![1639726473859](https://aeiblog-1301396258.cos.ap-chengdu.myqcloud.com/img/1639726473859.png)

这样划分出来的多边形就是有间隙

#### 多边形拆分

可以直接使用 difference 的 API 拆分

#### 多边形合并

采用凸包算法，进行地块间的合并

算法参考：

[算法细节系列（18）：凸包的三种计算*Demon-初来驾到-CSDN 博客*凸包算法](https://blog.csdn.net/u014688145/article/details/72200018/)

[凸包算法（Graham 扫描法） - 程序员大本营 (pianshen.com)](https://www.pianshen.com/article/763090525/)

[生成凸多边形 | Turf.js 中文网 (fenxianglu.cn)](https://turfjs.fenxianglu.cn/category/transformation/convex.html)
