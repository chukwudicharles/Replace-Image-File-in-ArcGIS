import arcpy
import os

def replace_images_in_aprx(folder_path, new_image_path):
    arcpy.AddMessage(f"Starting the interactive image replacement process for APRX files...")
    arcpy.AddMessage(f"Searching for APRX files in: {folder_path}")
    arcpy.AddMessage(f"Replacing images with: {new_image_path}")

    processed_count = 0
    replaced_count = 0
    error_count = 0

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".aprx"):
                aprx_path = os.path.join(root, file)
                arcpy.AddMessage(f"Processing APRX file: {aprx_path}")
                processed_count += 1

                try:
                    aprx = arcpy.mp.ArcGISProject(aprx_path)
                    for layout in aprx.listLayouts():
                        images_replaced_in_layout = 0
                        for element in layout.listElements("GRAPHIC_ELEMENT"):
                            
                            # Check if the the element has the 'elementSubType' attribute
                            if hasattr(element, 'elementSubType') and element.elementSubType == "Picture":
                            #if element.elementSubType == "Picture":
                                try:
                                    element.sourceImage = new_image_path
                                    arcpy.AddMessage(f"  Replaced image in layout '{layout.name}' element of: {aprx_path}")
                                    images_replaced_in_layout += 1
                                    replaced_count += 1
                                except Exception as e:
                                    arcpy.AddWarning(f"  Could not replace image in element '{element.name}' in layout '{layout.name}': {e}")
                                    
                        if images_replaced_in_layout > 0: # If at least an image was replaced in aprx layout
                             aprx.save()
                             arcpy.AddMessage(f"  Saved changes to layout(s) in: {aprx_path}")
                    del aprx
                except arcpy.ExecuteError:
                    arcpy.AddError(f"  ArcPy error processing {aprx_path}: {arcpy.GetMessages(2)}")
                    error_count += 1
                except Exception as e:
                    arcpy.AddError(f"  An error occurred while processing {aprx_path}: {e}")
                    error_count += 1

    arcpy.AddMessage(f"Interactive image replacement process for APRX files completed.")
    arcpy.AddMessage(f"Total APRX files processed: {processed_count}")
    arcpy.AddMessage(f"Total images replaced: {replaced_count}")
    if error_count > 0:
        arcpy.AddWarning(f"Total errors encountered: {error_count}")

if __name__ == "__main__":
    # Get the folder path from the user using arcpy.GetParameterAsText()
    folder_path = arcpy.GetParameterAsText(0)

    # Define the new image path
    new_image_path = r"\\gisfileintprd\Resources\Logos\WAPC\WAPC Logo Colour.png"

    # Call the function to replace images in APRX files
    replace_images_in_aprx(folder_path, new_image_path)