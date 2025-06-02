import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
#
# shelving/shelf.py
#     A simple program to draw a bookcase with measurements.
# 
# Author: Mike Smith
# Date: 31-05-2025  
# 
# Modification History:
#   M.R. Smith - 31-05-2025 - Initial version.
#   M.R. Smith - 02-06-2025 - Modified thickness from 24mm to 18mm and adjusted shelf heights.
#

# Variables and defaults.
x_pad = 10
y_pad = 10
tick_size = 3
materials = {}

# Defaults.
thickness = 1.8  # Thickness of the edges and uprights
plinth = 13  # Height of the plinth


def draw_width(ax, width):
    """
    Draw a horizontal arrow below the rectangle to indicate width.
    Parameters:
    - ax: The matplotlib axis to draw on.
    - width: The width of the rectangle.
    """

    # Draw width measurement
    arrow_y = y_pad - 5
    ax.annotate('', xy=(x_pad, arrow_y), xytext=(x_pad + width, arrow_y),
                arrowprops=dict(arrowstyle='<->', color='red', lw=1.5))
    ax.text(x_pad + width / 2, arrow_y - 2, f'{width} cm', ha='center', va='top', color='red', fontsize=10)

    # Width ticks
    ax.plot([x_pad, x_pad], [arrow_y - tick_size/2, arrow_y + tick_size/2], color='red', lw=1)
    ax.plot([x_pad + width, x_pad + width], [arrow_y - tick_size/2, arrow_y + tick_size/2], color='red', lw=1)


def draw_shelf_width(ax, plin_ht, edge_wd, lside_wt, divi_ln):
    """
    Draw a horizontal arrow above the first bottom shelf to indicate shelf width.
    Parameters:
    - ax: The matplotlib axis to draw on.
    - divi_ln: The width of the shelf.
    """

    # Draw shelf width measurement
    arrow_y = y_pad + 5 + plin_ht + edge_wd
    x_pad1 = x_pad + lside_wt
    width = divi_ln
    ax.annotate('', xy=(x_pad1, arrow_y), xytext=(x_pad1 + width, arrow_y),
                arrowprops=dict(arrowstyle='<->', color='red', lw=1.5))
    ax.text(x_pad1 + width / 2, arrow_y + 10, f'{width:0.1f} cm', ha='center', va='top', color='red', fontsize=10)

    # Width ticks
    #ax.plot([x_pad1, x_pad1], [arrow_y - tick_size/2, arrow_y + tick_size/2], color='red', lw=1)
    #ax.plot([x_pad1 + width, x_pad1 + width], [arrow_y - tick_size/2, arrow_y + tick_size/2], color='red', lw=1)


def draw_height(ax, height):
    """
    Draw a vertical arrow below the rectangle to indicate height.
    Parameters:
    - ax: The matplotlib axis to draw on.
    - height: The height of the rectangle.
    """

    # Draw height measurement
    arrow_x = x_pad - 5
    ax.annotate('', xy=(arrow_x, y_pad), xytext=(arrow_x, y_pad + height),
                arrowprops=dict(arrowstyle='<->', color='green', lw=1.5))
    ax.text(arrow_x - 2, y_pad + height / 2, f'{height} cm', ha='right', va='center', color='green', fontsize=10, rotation=90)
    # Height ticks
    ax.plot([arrow_x - tick_size/2, arrow_x + tick_size/2], [y_pad, y_pad], color='green', lw=1)
    ax.plot([arrow_x - tick_size/2, arrow_x + tick_size/2], [y_pad + height, y_pad + height], color='green', lw=1)




def draw_rectangle(ax, x, y, width, height, depth, fill=True):
    """
    Draw a rectangle on the given axis.
    
    Parameters:
    - ax: The matplotlib axis to draw on.
    - x: The x-coordinate of the bottom-left corner.
    - y: The y-coordinate of the bottom-left corner.
    - width: The width of the rectangle.
    - height: The height of the rectangle.
    - fill: Whether to fill the rectangle with color (default is True).
    """
    rect = Rectangle((x + x_pad, y + y_pad) , width, height, fill=fill)
    ax.add_patch(rect)

    # If the width is > 244 then add two items: 244 X height and remainder x height.
    if width == 2.4:
        width = depth
    if height == 2.4:
        height = depth

    if width > 244:
        remainder = width - 244
        add_to_materials(244, height)
        add_to_materials(remainder, height)
    else:
        if height > width:
            add_to_materials(height, width)
        else:
            add_to_materials(width, height)


def add_to_materials(width, height):
    """
    Add the dimensions of the rectangle to the materials dictionary.
    Parameters:
    - width: The width of the rectangle.
    - height: The height of the rectangle.
    """
    # Add to dictionary for later use
    key = f'{width:0.1f} x {height:0.1f}'
    if key in materials:
        materials[key] += 1
    else:   
        materials[key] = 1


def draw_bookcase(width, height, depth, edge_wd, shelf_heights, lside_wd, rside_wd, uprt_wd, plin_ht, top_ht, divides, title, fill, img_file='bookcase'):
    """
    Draw a bookcase with specified parameters.
    """
    materials.clear()  # Clear materials dictionary for each new bookcase

    # Calculate the length of the dividing sections.
    urights = divides - 1
    divi_ln = (width - lside_wd - rside_wd - urights * uprt_wd) / divides
    title = f'{title}'

    # Create a figure and axis.
    fig, ax = plt.subplots()
    #ax.set(xlim=(0, width), ylim=(0, height), xlabel='Length', ylabel='Height', title=title)
    ax.set(xlim=(0, width + x_pad), ylim=(0, height + y_pad), title=title)

    # Plinth.
    #ax.add_patch(Rectangle((0, 0), width, plin_ht, fill=fill))
    draw_rectangle(ax, 0, 0, width, plin_ht, depth, fill=fill)

    # Sides.
    if lside_wd > 0:
        #ax.add_patch(Rectangle((0, plin_ht), lside_wd, height-plin_ht, fill=fill))
        draw_rectangle(ax, 0, plin_ht, lside_wd, height-plin_ht, depth, fill=fill)
    if rside_wd > 0:
        #ax.add_patch(Rectangle((width-rside_wd, plin_ht), rside_wd, height-plin_ht, fill=fill))
        draw_rectangle(ax, width-rside_wd, plin_ht, rside_wd, height-plin_ht, depth, fill=fill)

    # Uprights.
    for i in range(1, divides):
        x = lside_wd + (i-1) * uprt_wd + i * divi_ln
        #ax.add_patch(Rectangle((x, plin_ht), uprt_wd, height-plin_ht, fill=fill))
        draw_rectangle(ax, x, plin_ht, uprt_wd, height-plin_ht, depth, fill=fill)
    
    # Bottoms
    for i in range (1, divides+1):
        x = lside_wd + (i-1) * (uprt_wd + divi_ln)
        #ax.add_patch(Rectangle((x, plin_ht), divi_ln, edge_wd, fill=fill))
        draw_rectangle(ax, x, plin_ht, divi_ln, edge_wd, depth, fill=fill)

    # Tops
    if top_ht > 0:
        for i in range (1, divides+1):
            x = lside_wd + (i-1) * (uprt_wd + divi_ln)
            #ax.add_patch(Rectangle((x, height-edge_wd), divi_ln, top_ht, fill=fill))
            draw_rectangle(ax, x, height-edge_wd, divi_ln, top_ht, depth, fill=fill)

    # Shelves
    #s_heights = [40, 40, 35, 35, 35]
    start = plin_ht + edge_wd
    for h in shelf_heights:
        y = start + h
        for i in range (1, divides+1):
            x = lside_wd + (i-1) * (uprt_wd + divi_ln)
            #ax.add_patch(Rectangle((x, y), divi_ln, edge_wd, fill=fill))
            draw_rectangle(ax, x, y, divi_ln, edge_wd, depth, fill=fill)
        start = y + edge_wd

    top_shelf = height - start - edge_wd
    print(f'Top shelf = {top_shelf:0.2f}')


    # Add measurement arrows

    # Horizontal measurement (width)
    draw_width(ax, width)

    # Vertical measurement (height)
    draw_height(ax, height)

    # Shelf width measurement (divi_ln)
    draw_shelf_width(ax, plin_ht, edge_wd, lside_wd, divi_ln)

    # these are matplotlib.patch.Patch properties
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)

    # place a text box in upper left in axes coords
    #textstr = f'Width: {width} cm\nHeight: {height} cm\nPlinth height: {plin_ht} cm\nDivides: {divides}\nShelf width: {divi_ln:.1f} cm'
    #textstr = f'Plinth height: {plin_ht:0.1f} cm'
    #ax.text(0.7, 1.06, textstr, transform=ax.transAxes, fontsize=10, verticalalignment='top', bbox=props)


    # List the materials used.
    mat_str = '\n'.join([f'{k}: {v}' for k, v in materials.items()])
    mat_str = f'Depth: {depth:0.1f} cm\nPlinth: {plin_ht:0.1f} cm\n\nMaterials used:\n{mat_str}'
    ax.text(1.02, 0.5, mat_str, transform=ax.transAxes, fontsize=10, verticalalignment='bottom', bbox=props)
    # Set the aspect of the plot to be equal, so the rectangle is not distorted.
    ax.set_aspect('equal', adjustable='box')
    # Set the limits of the plot to include padding around the rectangle.
    # Uncomment the next two lines to set limits with padding   

    #ax.set_xlim(0, x_pad + width + 20)
    #ax.set_ylim(0, y_pad + height + 20)  
    ax.set_xlim(0, 270) 
    ax.set_ylim(0, 280)  
    plt.axis('off')
    plt.tight_layout()
    plt.show()
    fig.savefig(f'{img_file}.png', facecolor=fig.get_facecolor(), edgecolor='none')


draw_bookcase(width=86.8, height=244+plinth, depth=30, shelf_heights=[40, 40, 35, 35, 35],
              edge_wd=thickness, lside_wd=thickness, rside_wd=0, uprt_wd=thickness, plin_ht=plinth, top_ht=0, divides=1, 
              title="Laundry ", fill=True, img_file='laundry')

draw_bookcase(width=259.4, height=244+plinth, depth=30, shelf_heights=[40, 40, 35, 35, 35],
              edge_wd=thickness, lside_wd=0, rside_wd=0, uprt_wd=thickness, plin_ht=plinth, top_ht=0, divides=3, 
              title="Kim's Study", fill=True, img_file='kim_study')

draw_bookcase(width=258.4, height=244+plinth, depth=21, shelf_heights=[38, 38, 35, 35, 35],
              edge_wd=thickness, lside_wd=thickness, rside_wd=thickness, uprt_wd=thickness, plin_ht=plinth, top_ht=thickness, divides=3, 
              title="Mikes's Studio 1", fill=True, img_file='mikes_studio1')

plinth = 17  # Height of the plinth
draw_bookcase(width=244.3, height=244+plinth, depth=42, shelf_heights=[34, 34, 34, 59.2, 34],
              edge_wd=thickness, lside_wd=thickness, rside_wd=thickness, uprt_wd=thickness, plin_ht=plinth, top_ht=thickness, divides=5, 
              title="Mikes's Studio 2", fill=True, img_file='mikes_studio2')


