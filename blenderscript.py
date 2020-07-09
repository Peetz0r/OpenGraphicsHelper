import bpy, os, io, sys, glob, json

from contextlib import redirect_stdout

models = os.scandir('models')

for model in models:
  if model.is_dir():
    obj = json.load(open(glob.glob('objects/**/*.'+model.name+'.json', recursive=True)[0]))
    print(' ➡ %s (%s)' % (obj['strings']['name']['en-GB'], model.name))

    if 'cars' in obj['properties']:
      for idx_car, car in enumerate(obj['properties']['cars']):
        print(' ➡ car %d/%d' % (idx_car, len(obj['properties']['cars'])))

        bpy.ops.wm.open_mainfile(filepath='Blender-RCT-Graphics/lighting_rig.blend')

        bpy.data.scenes[0].rct_graphics_helper_general_properties.output_directory = '%s/output/car-%d/' % (model.path, idx_car)

        fbx_file = '%s/car-%d.fbx' % (model.path, idx_car)
        print(' ➡ importing %s' % (fbx_file))

        with redirect_stdout(open(os.devnull, 'w')):
          bpy.ops.import_scene.fbx(filepath=fbx_file)

        flags = [
          'flat',
          'gentleSlopes',
          'steepSlopes',
          'verticalSlopes',
          'diagonalSlopes',
          'flatBanked',
          'gentleSlopeBankedTurns',
          'inlineTwists',
          'corkscrews',
          'curvedLiftHill',
        ]

        for idx_flag, flag in enumerate(flags):
          bpy.data.scenes['Scene'].rct_graphics_helper_vehicle_properties.sprite_track_flags[idx_flag] = flag in car['frames']
        bpy.data.scenes['Scene'].rct_graphics_helper_vehicle_properties.restraint_animation = 'restraintAnimation' in car['frames']

        bpy.ops.render.rct_vehicle()

    else:
      print(' ➡ no cars')
      bpy.ops.wm.open_mainfile(filepath='Blender-RCT-Graphics/lighting_rig.blend')

      fbx_file = glob.glob(model.path+'/*.fbx')[0]
      print(' ➡ importing %s' % (fbx_file))

      with redirect_stdout(open(os.devnull, 'w')):
        bpy.ops.import_scene.fbx(filepath=fbx_file)

      bpy.data.scenes[0].rct_graphics_helper_general_properties.output_directory = model.path + '/output/'
      bpy.data.scenes[0].rct_graphics_helper_static_properties['viewing_angles'] = 4

      bpy.ops.render.rct_static()

