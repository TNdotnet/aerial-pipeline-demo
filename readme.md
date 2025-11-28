- `demo1.py` – initialize a project folder layout (like a lightweight bootstrap), assists and logs labeling.
- `demo2.py` – simulate turning raw data into ready-data for user work with simple metadata.
- `demo3.py` – simulate generating labels and a dataset folder layout.
- `demo4.py` – simulate taking detection CSVs and turning them into JSON + a summary.

# Aerial Pipeline (Demo)

This repo is a **demo** of my aerial detection pipeline.  
The **full, production system** lives in a private repository; this public one just shows the structure and ideas.

## What the real project does

With **Ultralytics YOLO** and my setup, you can go from raw aerial imagery to a trained model and structured results:

- **Imagery → Tiles**  
  Scripts process aerial imagery into tiles ready for labeling.

- **Labeling helper**  
  - Opens Google Maps for the current tile so you get a second view.  
  - Logs your labeling activity and shows live label counts.

- **Training workflow**  
  - Builds YOLO training sets from your labels.  
  - Lets you **isolate subsets** if you labeled more than you need.  
  - Runs training with your chosen model/config.

- **Result “snowballing”**  
  - Takes model detections and turns them into a new labeled dataset.  
  - You can merge those new labels back into the original set and retrain.  
  - There are commands to export detections into a spreadsheet with coordinates, so you can join them to parcel IDs, addresses, etc.

- **Basic data management & safety**  
  - Commands to move/copy data between stages.  
  - Scripts create backups so if you “freestyle” and break things, you have a way back.

## Not implemented yet

- Merge detection locations into a standard table / database format (parcel IDs, addresses, etc.). Needs more research and some real-world schema examples.
- Generate Power BI instructions / templates based on that table, depending on market needs.
- Refactor into a more streamlined entry point (e.g. a single main script wrapping the steps).

  
## Example use case

> “I want to find new warehouses or new solar panels in the US.”

Day 1:
- Get the imagery.
- Run the pipeline to tiles.
- Label a first batch. **This is the only manual step; the setup handles the rest of the flow.**
- Train your first model.
- Run detections and export results with coordinates ready.
- Repeat with new imagery and merge new detections into your existing labeled set for the snowballing effect.

## Practical notes

- The original system was built for **US aerial data**.  
  I’ve tried some non-US sources; recent changes broke parts of the flow and I didn’t bother chasing them.

- You’ll need to adjust:
  - GPU / hardware settings in scripts for your machine.
- It **runs fine on AMD** with Ultralytics; that’s what I used.

- Storage:  
  I went with **1024×1024 tiles**, and hit ~**500 GB** with just three counties.  
  It’s tweakable, but expect it to be disk-hungry.

## This repo vs the private one

This public repo contains **demo scripts only** (no real geospatial math, no provider-specific details).  
Run them at your own risk or throw them in a chatbot.  
The private version includes the full production pipeline (around ~4000 lines of code).

I’d happily open the full project, but it was originally built while working with a specific company, and I don’t want to hand them a ready-made system they can just grab and reuse for free.

So:
- This repo shows the **shape of the pipeline** (scripts, flow, concepts).
- For now the **real geospatial logic, full automation, and production code** stay private.


## Demo pipeline overview

```mermaid
flowchart LR
    source[Raw input]
    demo2[demo2.py – turn raw into ready data]
    working[Working data for labeling]

    demo3_label[demo3.py – labels & dataset layout]
    train[Train model (outside this demo)]
    demo4[demo4.py – detections & summary]
    snowball[demo3.py – add labels from detections]

    demo1[demo1.py – layout + logging helper]

    source --> demo2 --> working --> demo3_label --> train --> demo4 --> snowball --> demo3_label
    demo1 --- source
    demo1 --- working
    demo1 --- demo3_label
